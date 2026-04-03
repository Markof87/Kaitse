from uuid import UUID

from app.application.dto.player import PlayerCreateDTO, PlayerFiltersDTO, PlayerNationalityAddDTO, PlayerPositionAddDTO, PlayerResponseDTO, PlayerUpdateDTO
from app.application.unit_of_work import UnitOfWork
from app.domain.exceptions import ConflictError, NotFoundError, ValidationError
from app.infrastructure.db.models.associations import PlayerNationality, PlayerPosition
from app.infrastructure.db.models.player import Player

class PlayerService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def get_by_id(self, player_id: UUID) -> PlayerResponseDTO:
        async with self.uow:
            player = await self.uow.players.get_by_id(player_id)
            if not player:
                raise NotFoundError(f"Player with id '{player_id}' not found", player_id)
            return PlayerResponseDTO.model_validate(player)
        
    async def get_by_slug(self, slug: str) -> PlayerResponseDTO:
        async with self.uow:
            player = await self.uow.players.get_by_slug(slug)
            if not player:
                raise NotFoundError(f"Player with slug '{slug}' not found", slug)
            return PlayerResponseDTO.model_validate(player)
        
    async def get_by_transfermarkt_id(self, transfermarkt_id: int) -> PlayerResponseDTO:
        async with self.uow:
            player = await self.uow.players.get_by_transfermarkt_id(transfermarkt_id)
            if not player:
                raise NotFoundError(f"Player with transfermarkt_id '{transfermarkt_id}' not found", transfermarkt_id)
            return PlayerResponseDTO.model_validate(player)
        
    async def list(self, filters: PlayerFiltersDTO) -> list[PlayerResponseDTO]:
        async with self.uow:
            players = await self.uow.players.list(filters.model_dump(exclude_none=True))
            return [PlayerResponseDTO.model_validate(player) for player in players]
        
    async def create(self, dto: PlayerCreateDTO) -> PlayerResponseDTO:
        async with self.uow:
            existing = await self.uow.players.get_by_slug(dto.slug)
            if existing:
                raise ConflictError(f"Player with slug '{dto.slug}' already exists", {"slug": dto.slug})
            player = Player(full_name=dto.full_name, 
                            short_name=dto.short_name,
                            birth_date=dto.birth_date, 
                            height=dto.height,
                            weight=dto.weight,
                            preferred_foot=dto.preferred_foot,
                            slug=dto.slug,
                            image_path=dto.image_path,
                            fbref_id=dto.fbref_id,
                            sofascore_id=dto.sofascore_id,
                            fotmob_id=dto.fotmob_id,
                            transfermarkt_id=dto.transfermarkt_id,
                        )
            saved = await self.uow.players.save(player)
            return PlayerResponseDTO.model_validate(saved)

    async def update(self, player_id: UUID, dto: PlayerUpdateDTO) -> PlayerResponseDTO:
        async with self.uow:
            player = await self.uow.players.get_by_id(player_id)
            if not player:
                raise NotFoundError(f"Player with id '{player_id}' not found", player_id)
            for field, value in dto.model_dump(exclude_none=True).items():
                setattr(player, field, value)
            saved = await self.uow.players.save(player)
            return PlayerResponseDTO.model_validate(saved)
        
    async def delete(self, player_id: UUID) -> None:
        async with self.uow:
            player = await self.uow.players.get_by_id(player_id)
            if not player:
                raise NotFoundError(f"Player with id '{player_id}' not found", player_id)
            await self.uow.players.delete(player_id)

    async def add_position(self, player_id: UUID, dto: PlayerPositionAddDTO) -> None:
        async with self.uow:
            player = await self.uow.players.get_by_id(player_id)
            if not player:
                raise NotFoundError(f"Player with id '{player_id}' not found", player_id)
            from sqlalchemy import select
            from app.infrastructure.db.models.associations import PlayerPosition

            #If is primary, check if player already has a primary position
            if dto.is_primary:
                result = await self.uow.session.execute(
                    select(PlayerPosition).where(PlayerPosition.player_id == player_id, PlayerPosition.is_primary == True)
                )
                if result.scalars().first():
                    raise ValidationError("Player already has a primary position", {"is_primary": "Player already has a primary position"})
            
            position = PlayerPosition(player_id=player_id, position_code=dto.position_code, is_primary=dto.is_primary)
            self .uow.session.add(position)
            await self.uow.session.flush()
    
    async def remove_position(self, player_id: UUID, position: str) -> None:
        async with self.uow:
            from sqlalchemy import select
            from app.infrastructure.db.models.associations import PlayerPosition
            result = await self.uow.session.execute(
                select(PlayerPosition).where(PlayerPosition.player_id == player_id, PlayerPosition.position_code == position)
            )
            player_position = result.scalars().first()
            if not player_position:
                raise NotFoundError(f"Position '{position}' for player with id '{player_id}' not found", {"position": position})
            await self.uow.session.delete(player_position)

    async def add_nationality(self, player_id: UUID, dto: PlayerNationalityAddDTO) -> None:
        async with self.uow:
            player = await self.uow.players.get_by_id(player_id)
            if not player:
                raise NotFoundError(f"Player with id '{player_id}' not found", player_id)
            from sqlalchemy import select
            from app.infrastructure.db.models.associations import PlayerNationality
            if dto.is_primary:
                result = await self.uow.session.execute(
                    select(PlayerNationality).where(PlayerNationality.player_id == player_id, PlayerNationality.is_primary == True)
                )
                if result.scalar_one_or_none():
                    raise ValidationError("Player already has a primary nationality", {"is_primary": "Player already has a primary nationality"})
            
            nationality = PlayerNationality(player_id=player_id, code=dto.code, is_primary=dto.is_primary)
            self.uow.session.add(nationality)
            await self.uow.session.flush()
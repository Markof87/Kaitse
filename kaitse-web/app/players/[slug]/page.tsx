import { supabasePublic } from "@/lib/supabasePublic";
import { notFound } from "next/navigation";

export const revalidate = 3600;

type PageProps = {
    params: Promise<{ slug: string }>;
};

export default async function PlayerPage({ params }: PageProps) {

    const { slug } = await params;

    const { data: player, error } = await supabasePublic
        .from("players")
        .select("id, full_name, short_name, birth_date, height_cm, weight_kg, preferred_foot, slug, image_path")
        .eq("slug", slug)
        .maybeSingle();

if (error || !player) notFound();

let imageUrl: string | null = null;

if (player.image_path) {
    imageUrl = `${process.env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/public/images/${player.image_path}`;
}

return (
<main style={{ fontFamily: "system-ui", padding: 24, maxWidth: 720 }}>
    <h1 style={{ marginBottom: 8 }}>{player.full_name}</h1>

    {imageUrl && (
    <img
        src={imageUrl}
        alt={player.full_name}
        style={{ width: 220, height: "auto", borderRadius: 12, display: "block", marginBottom: 16 }}
    />
    )}

    <ul>
        <li><b>Full name</b>: {player.full_name}</li>
        <li><b>Birth date</b>: {player.birth_date ?? "n/a"}</li>
        <li><b>Height</b>: {player.height_cm ?? "n/a"} cm</li>
        <li><b>Weight</b>: {player.weight_kg ?? "n/a"} kg</li>
        <li><b>Foot</b>: {player.preferred_foot ?? "n/a"}</li>
    </ul>
</main>
);
}
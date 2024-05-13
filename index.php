<!DOCTYPE html>
<html lang="fr-FR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="style.css" rel="stylesheet" />
    <link rel="icon" type="image/ico" href="logo_IMD.ico" />
    <title>Accueil</title>
</head>

<body>
    <header>
        <?php require_once "header.php"; ?>
    </header>

    <main>
    <h1>Derniers films</h1>
        <?php
        require_once "info_perso_db.php";

        try {
            $sql = "SELECT movie_id, title, overview, poster_path, price FROM movies ORDER BY release_date DESC";
            $stmt = $conn->prepare($sql);
            $stmt->execute();
            $films = $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            echo "Erreur lors de la requête : " . $e->getMessage();
            $films = [];
        }
        
        if (!empty($films)): ?>
            <div class="films-container">
                <?php foreach ($films as $film): ?>
                    <div class="film">
                        <img src="<?= htmlspecialchars($film['poster_path']) ?>" alt="<?= htmlspecialchars($film['title']) ?> Poster">
                        <h2><?= htmlspecialchars($film['title']) ?></h2>
                        <p><?= htmlspecialchars($film['overview']) ?></p>
                        <p>Prix: €<?= htmlspecialchars($film['price']) ?></p>
                        </div>
                <?php endforeach; ?>
            </div>
        <?php else: ?>
            <p>Aucun film trouvé.</p>
        <?php endif; ?>
    </main>

    <footer>
        <?php require_once "footer.php"; ?>
    </footer>
</body>

</html>
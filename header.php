<div class="logo">
    <a href="index.php"><img class="logo_header" src="image\logo_IMD.webp" alt="Logo" width="100em" height=""></a>
</div>
<div class="site_title">
    <a href="index.php" id="index"><span>IMD</span></a>
</div>
<div class="menu">
    <ul class="categories">
        <li><a href="action.php">Action</a></li>
        <li><a href="drama.php">Drama</a></li>
        <li><a href="science.php">Animation</a></li>
    </ul>
</div>
<div class="research">
    <form method="GET">
            <input type="search" name="utilisateur" placeholder="Look for a movie..." autocomplete="off" class="search_bar">
            <input type="submit" name="envoyer" class="search_sumbit">
    </form>
</div>
<div class="shopping">
    <a href="cart.php" class="cart_link" >
        <img class="shopping-cart-image" src="images\cart.png" alt="shopping cart">
<!--             <div class="cart-count"> $count = $bdd->query('SELECT COUNT(id) AS count FROM mymovie WHERE quantite > 0'); $rescount = $count->fetch (); echo($rescount['count'])  </div>
-->        </a>
</div> 
<div>
    <a href="deconnexion.php"><button class="login_btn">Logout</button></a>
</div>
        

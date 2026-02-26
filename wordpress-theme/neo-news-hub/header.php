<!doctype html>
<html <?php language_attributes(); ?>><head><meta charset="<?php bloginfo('charset');?>"><meta name="viewport" content="width=device-width,initial-scale=1">
<?php wp_head(); ?></head><body <?php body_class(); ?>>
<div class="topbar"><div class="inner"><div class="date" id="live-date"></div><div class="topics">AI &middot; Tech &middot; Innovation</div></div></div>
<header class="header"><div class="inner"><div class="masthead"><a href="<?php echo home_url('/'); ?>"><?php bloginfo('name'); ?></a></div>
<nav>
    <?php wp_nav_menu(array('theme_location'=>'primary','container'=>false,'menu_class'=>'menu')); ?>
    <button class="hamburger" id="hamburger">☰</button>
</nav>
</div></header>
<div class="container">
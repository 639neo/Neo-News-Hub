<?php
function neo_enqueue_assets(){
    wp_enqueue_style('neo-fonts','https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:wght@400;700&family=UnifrakturMaguntia&display=swap', array(), null);
    wp_enqueue_style('neo-style', get_stylesheet_uri());
    wp_enqueue_script('neo-main', get_template_directory_uri().'/js/main.js', array(), null, true);
}
add_action('wp_enqueue_scripts','neo_enqueue_assets');

function neo_setup(){
    add_theme_support('post-thumbnails');
    add_theme_support('title-tag');
    register_nav_menus(array('primary'=>'Primary Menu'));
}
add_action('after_setup_theme','neo_setup');
?>
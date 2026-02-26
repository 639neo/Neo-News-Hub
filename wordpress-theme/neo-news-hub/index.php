<?php get_header(); ?>
<?php
// Simple loop: show latest as hero
$latest = new WP_Query(array('posts_per_page'=>1));
if($latest->have_posts()): while($latest->have_posts()): $latest->the_post(); ?>
<div class="hero">
  <div class="image">
    <?php if(has_post_thumbnail()) the_post_thumbnail('large'); ?>
    <div class="tag-badge"><?php the_category(', '); ?></div>
  </div>
  <div class="lead">
    <h1 style="font-family:var(--font-display);font-size:48px"><?php the_title(); ?></h1>
    <p><?php the_excerpt(); ?></p>
    <a href="<?php the_permalink(); ?>">Read more →</a>
  </div>
</div>
<?php endwhile; wp_reset_postdata(); endif; ?>
<div class="posts-grid">
<?php $loop = new WP_Query(array('posts_per_page'=>9,'offset'=>1)); if($loop->have_posts()): while($loop->have_posts()): $loop->the_post(); ?>
<div class="card">
  <?php if(has_post_thumbnail()) the_post_thumbnail('medium'); ?>
  <div class="content">
    <div class="tag-badge"><?php the_category(', '); ?></div>
    <h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
    <p><?php echo wp_trim_words(get_the_excerpt(),20); ?></p>
  </div>
</div>
<?php endwhile; wp_reset_postdata(); endif; ?>
</div>
<?php get_footer(); ?>
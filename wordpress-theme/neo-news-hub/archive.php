<?php get_header(); ?>
<div class="container archive-list">
  <h1>All posts</h1>
  <?php if(have_posts()): while(have_posts()): the_post(); ?>
    <div class="item">
      <?php if(has_post_thumbnail()) the_post_thumbnail('thumbnail'); ?>
      <div>
        <h3><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h3>
        <p><?php echo wp_trim_words(get_the_excerpt(),30); ?></p>
      </div>
    </div>
  <?php endwhile; endif; ?>
</div>
<?php get_footer(); ?>
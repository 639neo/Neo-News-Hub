<?php get_header(); ?>
<div class="single">
  <div class="content">
    <?php if(have_posts()): while(have_posts()): the_post(); ?>
      <div class="breadcrumb"><a href="<?php echo home_url('/'); ?>">Home</a> &raquo; <?php the_title(); ?></div>
      <div class="meta"><?php the_date(); ?> | <?php the_author(); ?></div>
      <h1 style="font-family:var(--font-display);font-size:36px"><?php the_title(); ?></h1>
      <?php if(has_post_thumbnail()) the_post_thumbnail('large'); ?>
      <div class="entry"><?php the_content(); ?></div>
      <div class="tags"><?php the_tags('Tags: ',', '); ?></div>
    <?php endwhile; endif; ?>
    <h3>Recent posts</h3>
    <ul>
    <?php $rp = new WP_Query(array('posts_per_page'=>5)); while($rp->have_posts()): $rp->the_post(); ?>
      <li><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></li>
    <?php endwhile; wp_reset_postdata(); ?>
    </ul>
  </div>
</div>
<?php get_footer(); ?>
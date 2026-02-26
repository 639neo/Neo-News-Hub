document.addEventListener('DOMContentLoaded',function(){
  var ham=document.getElementById('hamburger');if(ham){ham.addEventListener('click',function(){var m=document.querySelector('nav .menu');if(m.style.display==='block'){m.style.display='flex';}else{m.style.display='block';m.style.flexDirection='column';m.style.background='var(--black)';m.style.color='var(--white)'}})}
  var d=document.getElementById('live-date'); if(d){d.textContent=new Date().toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric',year:'numeric'})}
});
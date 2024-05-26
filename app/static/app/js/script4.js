$(document).ready(function () {
    $(".filter-item").click(function () {
        const value = $(this).attr("data-filter");
        if (value == "all"){
            $(".postt-box").show("1000")
        } else{
            $(".postt-box")
                .not("." + value)
                .hide(1000);
            $(".postt-box")
            .filter("." + value)
            .show("1000")
        }
    });
    $(".filter-item").click(function () {
        $(this).addClass("active-filter").siblings().removeClass("active-filter")
    });
  });
  
  var topp=document.querySelector('.top');
  window.addEventListener('scroll',activeNavbar)
  function activeNavbar(){
  var x = this.pageYOffset;
      if(x>80){
          topp.classList.add('active2');
      }
      else{
          topp.classList.remove('active2');
      }    
  };
  
  let navbar=document.querySelector('.icons');
  let searchbox=document.querySelector('.search-box .fa-magnifying-glass');
  searchbox.addEventListener('click',()=>{
      navbar.classList.toggle('showInput');
      if(navbar.classList.contains('showInput')){
          searchbox.classList.replace("fa-magnifying-glass","fa-x");
      }else{
          searchbox.classList.replace("fa-x","fa-magnifying-glass")
      }
  })
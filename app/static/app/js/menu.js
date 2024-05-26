

var topp=document.querySelector('.top');
window.addEventListener('scroll',activeNavbar)
function activeNavbar(){
var x = this.pageYOffset;
    if(x>80){
        topp.classList.add('active3');
    }
    else{
        topp.classList.remove('active3');
    }    
};


//<i class="fa-solid fa-x"></i>
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

const menuTile=document.querySelector('.menu-title');
const menuTile2=document.querySelector('.menu-title');
menuTile.addEventListener('click',function(x){
    if(x.target.classList.contains('menu_btn')){
        const Target =x.target.getAttribute('data-a');
        menuTile.querySelector('.active2').classList.remove('active2');
        x.target.classList.add('active2');
        
        const menuItem=document.querySelector('.menu');
        menuItem.querySelector('.menu_item_content.active2').classList.remove('active2');
        menuItem.querySelector(Target).classList.add("active2");
        
    }
});

menuTile2.addEventListener('click',function(y){
    if(y.target.classList.contains('menu_btn')){
        menuTile2.querySelector('.active').classList.remove('active');
        y.target.classList.add('active');
    }
})

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

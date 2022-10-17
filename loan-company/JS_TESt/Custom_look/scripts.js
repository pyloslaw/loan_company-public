let nav = document.getElementById('navbar').classList;
let menu = document.getElementById('menu-ic').classList;
let closeMen = document.getElementById('close-ic').classList;



function openMenu() {

    if (nav.contains('menu-invisible') && closeMen.contains('menu-invisible')) {
        var cl = nav.remove('menu-invisible'); closeMen.remove('menu-invisible'); menu.add('menu-invisible');
        return cl
    } else {
        var op =  nav.add('menu-invisible'); closeMen.add('menu-invisible'); menu.remove('menu-invisible');
        return op
       
    }
}
document.addEventListener('DOMContentLoaded', function() {
    var toggleNavbarBtnClub = document.getElementById('toggle-navbar-club');
    var navbarClub = document.getElementById('navbar-club');
    
    var toggleNavbarBtnEstadios = document.getElementById('toggle-navbar-estadios');
    var navbarEstadios = document.getElementById('navbar-estadios');
    
    var toggleNavbarBtnCompeticiones = document.getElementById('toggle-navbar-competiciones');
    var navbarCompeticiones = document.getElementById('navbar-competiciones');

    function hideAllNavbars() {
        navbarClub.style.display = 'none';
        navbarEstadios.style.display = 'none';
        navbarCompeticiones.style.display = 'none';
    }

    toggleNavbarBtnClub.addEventListener('click', function() {

        if (navbarClub.style.display === 'block') {
            navbarClub.style.display = 'none';
        } else {
            hideAllNavbars();
            navbarClub.style.display = 'block';
        }
    });

    toggleNavbarBtnEstadios.addEventListener('click', function() {

        if (navbarEstadios.style.display === 'block') {
            navbarEstadios.style.display = 'none';
        } else {
            hideAllNavbars();
            navbarEstadios.style.display = 'block';
        }
    });

    toggleNavbarBtnCompeticiones.addEventListener('click', function() {

        if (navbarCompeticiones.style.display === 'block') {
            navbarCompeticiones.style.display = 'none';
        } else {
            hideAllNavbars();
            navbarCompeticiones.style.display = 'block';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var toggleNavbarBtn = document.getElementById('toggle-navbar');
    var navbar = document.getElementById('navbar');

    toggleNavbarBtn.addEventListener('click', function() {
        navbar.style.display = (navbar.style.display === 'block') ? 'none' : 'block';
    });
});
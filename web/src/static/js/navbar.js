document.addEventListener('DOMContentLoaded', function() {
    var toggleNavbarBtnPartidos = document.getElementById('toggle-navbar-partidos');
    var navbarPartidos = document.getElementById('navbar-partidos');
    
    var toggleNavbarBtnEquipos = document.getElementById('toggle-navbar-equipos');
    var navbarEquipos = document.getElementById('navbar-equipos');
    
    var toggleNavbarBtnJugadores = document.getElementById('toggle-navbar-jugadores');
    var navbarJugadores = document.getElementById('navbar-jugadores');
    
    var toggleNavbarBtnEstadios = document.getElementById('toggle-navbar-estadios');
    var navbarEstadios = document.getElementById('navbar-estadios');
    
    var toggleNavbarBtnCompeticiones = document.getElementById('toggle-navbar-competiciones');
    var navbarCompeticiones = document.getElementById('navbar-competiciones');

    function hideAllNavbars() {
        navbarPartidos.style.display = 'none';
        navbarEquipos.style.display = 'none';
        navbarJugadores.style.display = 'none';
        navbarEstadios.style.display = 'none';
        navbarCompeticiones.style.display = 'none';
    }

    toggleNavbarBtnPartidos.addEventListener('click', function() {

        if (navbarPartidos.style.display === 'block') {
            navbarPartidos.style.display = 'none';
        } else {
            hideAllNavbars();
            navbarPartidos.style.display = 'block';
        }
    });

    toggleNavbarBtnEquipos.addEventListener('click', function() {

        if (navbarEquipos.style.display === 'block') {
            navbarEquipos.style.display = 'none';
        } else {
            hideAllNavbars();
            navbarEquipos.style.display = 'block';
        }
    });

    toggleNavbarBtnJugadores.addEventListener('click', function() {

        if (navbarJugadores.style.display === 'block') {
            navbarJugadores.style.display = 'none';
        } else {
            hideAllNavbars();
            navbarJugadores.style.display = 'block';
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
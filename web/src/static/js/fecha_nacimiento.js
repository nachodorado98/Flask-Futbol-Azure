const today=new Date();

const yyyy=today.getFullYear();
const mm=String(today.getMonth()+1).padStart(2, '0');
const dd=String(today.getDate()).padStart(2, '0');

let maxYear=yyyy-18;
let maxDate=`${maxYear}-${mm}-${dd}`;

if (mm==="02" && dd==="29") {
    if (!((maxYear%4===0 && maxYear% 100!==0) || (maxYear%400===0))) {
        maxDate=`${maxYear}-02-28`;
    }
}

document.getElementById("fecha-nacimiento").setAttribute("min", "1900-01-01");
document.getElementById("fecha-nacimiento").setAttribute("max", maxDate);
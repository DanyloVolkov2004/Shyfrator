// FRONT-END \\

let CiperButt=document.getElementById("CiperButt");
let SaveButt=document.getElementById("SaveButt");

CiperButt.onclick=function(){
    CiperButt.className="button1 disable";
    SaveButt.className="button1 "
}

SaveButt.onclick=function(){
    SaveButt.className="button1 disable";
    CiperButt.className="button1 "
}


// BACK-END \\

// Open file dialog
document.getElementById("openFile").addEventListener("click", () => {
    eel.open_file_dialog(); 
})
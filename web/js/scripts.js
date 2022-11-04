// FRONT-END \\

let wrapper=document.getElementById("wrapper");
let CipherPageBtn=document.getElementById('CipherPageBtn');
let CiperButt=document.getElementById("CiperButt");
let SaveButt=document.getElementById("SaveButt");

let MenuPage=document.getElementById("menu");
let CiepherPage=document.getElementById("CiepherPage");

CipherPageBtn.onclick=OpenCiepherPage;

function OpenCiepherPage(){
    MenuPage.style.display="none"
    CiepherPage.style.display="block"
}

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
    eel.get_file_path(); 
})

// Select cipher
document.getElementById("metod").addEventListener("change", (event) => {
    eel.get_method(event.target.value);
})

// Select password
document.getElementById("key").addEventListener("change", (event) => {
    eel.get_password(event.target.value); 
})

// Encode
document.getElementById("CiperButt").addEventListener("click", () => {
    eel.encode();
})
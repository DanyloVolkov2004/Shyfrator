// FRONT-END \\

let wrapper=document.getElementById("wrapper");



//Buttons\\
let CipherPageBtn=document.getElementById('CipherPageBtn');
let DecipherPageBtn=document.getElementById('DecipherPageBtn');
let CiperButt=document.getElementById("CiperButt");
let SaveButt=document.getElementById("SaveButt");
let DecipherButt=document.getElementById("DecipherButt");
let DecipherSaveButt=document.getElementById("DecipherSaveButt");


//Pages\\
let MenuPage=document.getElementById("menu");
let CiepherPage=document.getElementById("CiepherPage");
let DecipherPage=document.getElementById("DeciepherPage");

//Error Messages\\
let ErrorMessages=document.getElementsByClassName("error_message");

CipherPageBtn.onclick=OpenCiepherPage;
DecipherPageBtn.onclick=OpenDeciepherPage;



function OpenCiepherPage(){
    MenuPage.style.display="none"
    CiepherPage.style.display="block"
}
function OpenDeciepherPage(){
    MenuPage.style.display="none"
    DecipherPage.style.display="block"
}


//Function to make all error messages visible\\
function MakeAllElementsVisible(elements){

    for(let i=0;i<elements.length;i++){
        elements[i].style.display="block";
    }
}

CiperButt.onclick=function(){
    CiperButt.className="button1 disable";
    SaveButt.className="button1 "
}

SaveButt.onclick=function(){
    SaveButt.className="button1 disable";
    CiperButt.className="button1 "
}

DecipherButt.onclick=function(){
    DecipherButt.className="button1 disable";
    DecipherSaveButt.className="button1 "
}

DecipherSaveButt.onclick=function(){
    DecipherSaveButt.className="button1 disable";
    DecipherButt.className="button1 "
}






// BACK-END \\

// Open file dialog for encoding
document.getElementById("openFileForEncoding").addEventListener("click", () => {
    eel.get_encription_file_path(); 
})

// Open file dialog for decoding
document.getElementById("openFileForDecoding").addEventListener("click", () => {
    eel.get_decription_file_path(); 
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

// Save file
document.getElementById("SaveButt").addEventListener("click", () => {
    eel.save_file_to();
})
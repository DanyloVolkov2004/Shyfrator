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

}

SaveButt.onclick=function(){

}

DecipherButt.onclick=function(){
    
}

DecipherSaveButt.onclick=function(){

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
document.querySelectorAll(".metod").forEach(item => {
    item.addEventListener("change", (event) => {
        eel.get_method(event.target.value); 
    })
})

// Select password
document.querySelectorAll(".key").forEach(item => {
    item.addEventListener("change", (event) => {
        eel.get_password(event.target.value); 
    })
})

// Encode
document.getElementById("CiperButt").addEventListener("click", async () => {
    let response = await eel.encode()();
    let json = JSON.parse(response);
    if (json["success"] == false) {
        alert(json["message"]);
    }
    else {
        CiperButt.disabled = true;
        SaveButt.disabled = false;
        CiperButt.className = "button1 disable";
        SaveButt.className = "button1 ";
    }

})

// Decode
document.getElementById("DecipherButt").addEventListener("click", async () => {
    let response = await eel.decode()();
    let json = JSON.parse(response);
    if (json["success"] == false) {
        alert(json["message"]);
    }
    else {
        DecipherButt.disabled = true;
        DecipherSaveButt.disabled = false;
        DecipherButt.className="button1 disable";
        DecipherSaveButt.className="button1 ";
    }
})

// Save file
document.getElementById("SaveButt").addEventListener("click", async () => {
    let response = await eel.save_file_to()();
    let json = JSON.parse(response);
    if (json["success"] == false) {
        alert(json["message"]);
    } 
    else {
        CiperButt.disabled = false;
        SaveButt.disabled = true;
        SaveButt.className="button1 disable";
        CiperButt.className="button1 ";
    }
})

// Save file
document.getElementById("DecipherSaveButt").addEventListener("click", async () => {
    let response = await eel.save_file_to()();
    let json = JSON.parse(response);
    if (json["success"] == false) {
        alert(json["message"]);
    }
    else {
        DecipherButt.disabled = false;
        DecipherSaveButt.disabled = true;
        DecipherSaveButt.className="button1 disable";
        DecipherButt.className="button1 ";
    }
})

// I dont know what is better to use with or without async
// document.getElementById("get").addEventListener("click", () => {
//     document.getElementById("text").innerText = eel.get_proba()();
// })

// get data from python
document.getElementById("get").addEventListener("click", async() => {
    document.getElementById("text").innerText = await eel.get_proba()();
})

// send data to python
document.getElementById("send").addEventListener("click", async() => {
    await eel.send_proba("PROBAAAA")
})
document.querySelector("#cancel-btn").addEventListener("click", (e) => {
    e.preventDefault();
  console.log("Cancel button clicked");
  document.querySelector("#modal-bg").style.display = "none";
});



document.querySelector("#cancel-btn2").addEventListener("click", (e) => {
    e.preventDefault();
    console.log("Cancel button clicked");
    document.querySelector("#modal-bg").style.display = "none";
  });


document.querySelector("#add-class").addEventListener("click", () => {
    document.querySelector("#modal-bg").style.display = "flex";
    });

document.querySelector("#add-sub").addEventListener("click", (e) => {
    e.preventDefault();
    document.querySelector("#form-header").innerHTML = `<div class="form-header">
    <div class="input large-input">
        <input type="text" placeholder="Subjects" data-placeholder="E-mail" >
        
    </div>

    <div class="input large-input">
        <input type="text"  class="input-mat"  placeholder="Lectures" data-placeholder="E-mail" >
    </div>
</div>` + document.querySelector("#form-header").innerHTML;
    });
    
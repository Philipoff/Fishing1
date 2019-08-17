const input = document.getElementByld('search');
input.addEventListener('keyup',() => {
    const filter = input.value.toUpperCase(),
        ul = document.getElementByld("students"),
        li = ul.getElementsByTagName('li');

    for (i=0, i < li.length; i++) {
    let a = li[i].getElementsByTagName("a")[0];
     if (a.innerHTML.toUpperCase().indexOf(filter) > -1){
     li[i].style.display = "";
     } else {
      li[i].style.display = "none";}
      }
    }
})
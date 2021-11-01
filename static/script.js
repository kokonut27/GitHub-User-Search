function SearchFunction() {
  // let searchbtn = document.getElementById("searchbtn");
  let searchvalue = document.getElementById("searchval").value;

  $.post( "/searchvalue", {
    data: searchvalue
  });
};
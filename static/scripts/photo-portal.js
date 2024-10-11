function validate_data() {

  const validData = true; 
  const search_select_val = document.getElementById("search_select").value;
  
  // R5.2.1 Check Date  
  if (search_select_val === "Date") {
    const search_input_val = document.getElementById("search_input").value;
    date_regex = /^\d{2}\/\d{2}\/\d{4}$/;
    if (!search_input_val.match(date_regex)) {
      alert("Date format should be MM/DD/YYYY.");
      validData = false; 
    } 
  }

  // R5.2.2 Check Name
  else if (search_select_val === "Name") {
    const search_input_val = document.getElementById("search_input").value;
    if (search_input_val === "") {
      alert("Name should not be empty.");
      validData = false;
    } 
  }

  // R5.2.3 Check Tags
  else {
    const search_input_val = document.getElementById("search_input").value;
    if (search_input_val === "") {
      alert("Tags should not be empty.");
      validData = false;
    } 
  }
  
  return validData;

}

function show_photo_details(photo_name, date_taken, tags) {
  alert("Photo:" + photo_name + " date_taken:" + date_taken + " tags:" + tags);
}


// ASSIGNMENT 2 -- Implement the preview_photo method that displays the photo in modal (R4.3)
function preview_photo(photo_name) {

  photo_ele = document.createElement('img');
  photo_ele.setAttribute("id", "preview-image");
  photo_ele.src = "..//static/images/photos/" + photo_name;

  photo_ele.onload = () => {
    URL.revokeObjectURL(photo_ele.src);
  }
  modal = document.getElementById("image-modal-body");
  modal.appendChild(photo_ele);

}


function show_settings() {
  alert("Settings called.");
}

function logout() {
  document.getElementById("settings-and-logout-form").submit();
}

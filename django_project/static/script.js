function hide_show_table(col_name, url, token) {
    let i, all_col;
    let checkbox_val = document.getElementById(col_name).value;
    if (checkbox_val === "hide") {
        all_col = document.getElementsByClassName(col_name);
        for (i = 0; i < all_col.length; i++) {
            all_col[i].style.display = "none";
        }
        document.getElementById(col_name + "_head").style.display = "none";
        document.getElementById(col_name).value = "show";
    } else {
        all_col = document.getElementsByClassName(col_name);
        for (i = 0; i < all_col.length; i++) {
            all_col[i].style.display = "table-cell";
        }
        document.getElementById(col_name + "_head").style.display = "table-cell";
        document.getElementById(col_name).value = "hide";
    }

    $.ajax({
            url: url,
            type: "POST",
            data: {column_name: col_name, column_value: checkbox_val, "csrfmiddlewaretoken": token}
        }
    );
}
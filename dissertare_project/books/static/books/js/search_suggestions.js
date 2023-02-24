// container da barra de pesquisa
const searchWrapper = document.querySelector('.search');
// barra de pesquisa
const inputBox = document.querySelector('.search-input');
// lista de sugestões
const suggestBox = searchWrapper.querySelector('.suggestion-list');


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

inputBox.onkeyup = (e)=> {
    let userData = e.target.value;
    let suggestions;
    let emptyArray = [];

    if(userData) {
        const formData = JSON.stringify({'val': userData})
        const csrftoken = getCookie('csrftoken');

        const option = {
            method: 'POST',
            headers: {
                "Accept": 'application/json',
                "X-Requested-With": 'XMLHttpRequest',
                "X-CSRFToken": csrftoken
            },
            body: formData,
            mode: 'same-origin'
        }

        fetch('search_suggestions/', option)
        .then (response => {
            if (!response.ok) {
                return new Error("Falhou a requisição!")
            }

            if (response.status === 404) {
                return new Error("Não encontrou qualquer resultado")
            }

            return response.json()
        })
        .then(data => {
            console.log(data)
        })
        .catch(err => {
            console.log(err)
        })

        emptyArray = suggestions.filter((data) =>{
            return data.toLocaleLowerCase().startsWith(userData.toLocaleLowerCase());
        })
        emptyArray = emptyArray.map((data) => {
            return data = `<li>${data}</li>`;
        })
        suggestBox.classList.add('active');
        ShowSuggestions(emptyArray);
        let allList = suggestBox.querySelectorAll('li');
        for (let i = 0; i < allList.length; i++) {
            allList[i].setAttribute('onclick', 'select(this)');
        }

        if(e.key === 'Escape') {
            suggestBox.classList.remove('active');
        }
    } else {
        suggestBox.classList.remove('active');
        suggestBox.innerHTML = ''
    }
}

function select(element) {
    let selectData = element.textContent;
    inputBox.value = selectData;
    
    suggestBox.classList.remove('active');
}

function ShowSuggestions(list) {
    let listData;

    if(!list.length) {
        userValue = inputBox.value;
        listData = `<li>${userData}</li>`
    } else {
        listData = list.join('');
    }

    suggestBox.innerHTML = listData;
}
///// get all update-cart classes
var updateButtons =  document.getElementsByClassName('update-cart');

/// add eventListener for all update-class clicked

for(let i =0; i<updateButtons.length;i++){
    updateButtons[i].addEventListener('click',function(){
        // get value of data-product and data-action
        var productId =  this.dataset.product;
        var action = this.dataset.action
        console.log("user"+user)
        if(user=== `AnonymousUser`){
           // console.log('not logged in')
           addCookieItem(productId,action)
        }
        else{
            updateUserOrder(productId,action)
        }
        console.log("proudctId "+productId);
    })
}

function addCookieItem(productId,action){

    if(action == "add"){
        // check if that productId doesnt exists
        if(cart[productId] == undefined){
            ///create it
            cart[productId] = {'quantity':1}

        }else{
            cart[productId]['quantity']+=1;
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity'] -=1;

        if(cart[productId]['quantity']<=0){
            console.log("remove item");

            delete cart[productId]
        }
    }

    console.log(cart);
    document.cookie = 'cart='+JSON.stringify(cart) + ";domian=;path=/"

}

function updateUserOrder(productId,action){

    var url = '/update_item/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId':productId,'action':action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data',data)
        location.reload()
    })

}
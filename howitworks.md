# How it works
So the main piece to this project was [git_api](https://github.com/JBYT27/GitAPI), which is a package I created to retrieve GitHub stats through python. The next main piece to this project is sending and retrieving requests and data, which @Highwayman explained to me very thoroughly (thanks ^^) [here](https://replit.com/talk/ask/How-to-retrieving-JavaScript-variable-data-using-Python/147113). The final piece was the CSS and the HTML, which was basically all markup or styling. To explain it much, much, *much* thoroughly, read below. Also, thanks to @DillonB07 for helping me test some errors and solve some errors!

### The very thorough explanation ^^
So the first part to this project was git_api, mentioned before above. git_api is a package that retrieves GitHub data through queries and graphql, which can be read about [here](https://docs.github.com/en/graphql). By using git_api, I could retrieve github data very successfully, however I stumbled upon a big roadblock that frankly, stumped me for a while.


This roadblock was the process of sending data using JavaScript, and then retrieving it using Python [Flask]. I'm not the best with Flask, so it took me a while to get the solution. 

First, I tried [posting](https://replit.com/talk/ask/How-to-retrieving-JavaScript-variable-data-using-Python/147113) in Replit, and I did get a explanation, which helped me, but I still didn't know how to do that in Python and JavaScript. I ran across a post in Stack Overflow (Yes, I know. Don't blame me, I was using worse case senario actions lol) that pretty much had the solution. ~~Forgive me for not having the link, as it's somewhere in my search history LOL.~~ 

The solution was basically this short code that's written below, and now, all I had to do was retrieve it using python flask, which this part, I could do much easily.

```js
function SearchFunction() {
  // let searchbtn = document.getElementById("searchbtn");
  let searchvalue = document.getElementById("searchval").value;
  // alert(searchvalue)
        
  $.post( "/searchvalue", {
    data: searchvalue
  });
};
```

> What this code does is that it first retrieves the HTML value returned from the input where you enter the GitHub username. Then, the `$.post` part is jquery, and what that does is post the value into a route in the website, created by flask (and yours truly).

Now, all I had to do was retrieve the value using flask. This was a bit easier, as there is already a built in function that Flask has made. I had to first create a `POST` route, and then an addition `GET` route, for the route to actually be accessible route. The following code kind of explains the steps above and what I had to do this step.

```py
@app.route('/search')
def search():
  return render_template(
    "search.html",
    ...
  )


@app.route('/searchvalue', methods=["POST", "GET"])
def searchvalue():
  if request.method == "POST":
    ...
```

> So the code here is what you could call the "retrieving the JavaScript data and etc". So probably, the most obvious thing you see here is the `methods=["POST", "GET"]`. This is the `POST` request, and basically, it allows us to retrieve data. But wait, where's the function that gets all the data. And where *is* the data? To answer that, it isn't shown here, but I'll show it down below. When you do the `POST` request for the route, it practically does it all for you. The only thing left for you to do is to retrieve it with the one function: `request.form["data"]`. Do you remember our old function from the JavaScript code? Well, this is where it all pieces together. The `$.post( "/searchvalue", {data: searchvalue});` is where it posts the value, and look! The route `/searchvalue` is in the Python code. And the `data: searchvalue` has the key `data` in it, which is where we use `request.form["data"]`. So basically, the JavaScript code sends a `POST` request that sends data, and then Python retrieves the `POST` request and successfully gets the data, ready to use.

Okay, so now I'm over the roadblock. Basically, I don't think I really need to explain this bit part of the project, but really, I just added markup and styling to the project to make it more professional like, real-life use-like, and project-usable. Sorry for my super long explanation, but I hope it explains how I coded this project!

> For more about Flask, look at the document [here](https://flask.palletsprojects.com/en/2.0.x/).
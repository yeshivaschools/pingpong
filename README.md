# pingpong
#### 2D Ping Pong game
![preview image](https://cdn.discordapp.com/attachments/765617233497161830/901890664315383908/unknown.png)
___
### How to play:
* player 1
    * `w` To move **up**
    * `s` To move **Down**
* player 2
    * `up` To move **up**
    * `down` To move **Down**
* Press `Space` to **serve**
* Settings documentation
    * Input **1**: window `width, height`
        * `width`: The width of the window (500 ≤ `width` ≤ 20000)
        * `height`: The height of the window (300 ≤ `height` ≤ 12000)
    * Input **2**: robot `player, view`
        * `player`: The player that the robot will control (1 or 2 (0 for pvp))
        * `view`: the view of the robot (1 ≤ `view` ≤ 3)
    * Input **3**: ball `speed, radius`
        * `speed`: The speed of the ball (1 ≤ `speed` ≤ 12)
        * `radius`: The radius of the ball (2 ≤ `radius` ≤ 400)
    * Input **4**: p1 `width, height, speed`
        * `width`: The width of the paddle (1 ≤ `width` ≤ 250)
        * `height`: The height of the paddle (1 ≤ `height` ≤ 500)
        * `speed`: The speed of the paddle (1 ≤ `speed` ≤ 50)
    * Input **5**: p2 `width, height, speed`
        * `width`: The width of the paddle (1 ≤ `width` ≤ 250)
        * `height`: The height of the paddle (1 ≤ `height` ≤ 500)
        * `speed`: The speed of the paddle (1 ≤ `speed` ≤ 50)
### Format the input so that the values are seperated by only a comma.
##### `w`: Width, `h`: Height, `s`: Speed, `p`: Player, `v`: View
#### To change the other game settings, you can change the values in the `./settings.json` file.
___
[aroary](https://github.com/aroary) | [replit](https://replit.com/@aroary4444/pingpong)

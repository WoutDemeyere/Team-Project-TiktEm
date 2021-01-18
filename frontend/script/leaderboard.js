var filterArray = [];

const loadLeaderboard = async (leaderboard, game, length=null, filter=null) => {
    const data = await fetch(
            `http://${lanIP}/tiktem/v1/leaderboard/${game}`
        )
        .then((r) => r.json())
        .catch((err) => console.error("An error occurd", err));
    console.log(data);
    loadLeaderboardHTML(leaderboard, data, length, filter);
}

const loadLeaderboardHTML = (leaderboard, data, length=null, filter=null) => {
    if(length==null) length=data.length;

    data[0].scortype="t"?prefix="s":prefix=""

    console.log(filter)

    htmlString = `  <tr class="c-table-header">
                        <th class="c-table-header__text">Plaats</th>
                        <th class="c-table-header__text">Naam</th>
                        <th class="c-table-header__text">Score</th>
                    </tr>`;

    if(!isEmpty(filter)) {
        for(const d of data) {
            if(d.name.search(filter) > -1)filterArray.push(d)
            console.log(d.name)
        }
        
    } else {
        for(var i = 0; i < length; i++) {
            if(i < 3) {
                htmlString += ` <tr class="c-table-row c-talbe-row-${i+1}">
                                    <td class="c-table-row-text">${i+1}</td>
                                    <td class="c-table-row-text">${data[i].name}</td>
                                    <td class="c-table-row-text">${data[i].score + prefix}</td>
                                </tr>`
            } else {
                htmlString += ` <tr class="c-table-row">
                                    <td class="c-table-row-text">${i+1}</td>
                                    <td class="c-table-row-text">${data[i].name}</td>
                                    <td class="c-table-row-text">${data[i].score + prefix}</td>
                                </tr>`
            }
        }
    }
    
    leaderboard.innerHTML = htmlString;
}


const isEmpty = function (fieldValue) {
    return !fieldValue || !fieldValue.length;
};
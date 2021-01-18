var filterArray = [];

class Leaderboard {
    constructor(leaderBoardContainer, game, length=null) {
        this.container = leaderBoardContainer
        this.game = game
        this.data = 0
        this.length = length
        this.htmlString = ``
        this.prefix = ""
    }

    async loadLeaderboardData() {
        this.data = await fetch(
            `http://${lanIP}/tiktem/v1/leaderboard/${this.game}`
        )
        .then((r) => r.json())
        .catch((err) => console.error("An error occurd", err));
        console.log(this.data);
        this.loadLeaderboardHTML();
    }

    loadLeaderboardHTML() {
        if(!this.length)this.length=this.data.length;

        this.data[0].scortype="t"?this.prefix="s":this.refix=""

        // console.log(this.container)

        this.htmlString = `  <tr class="c-table-header">
                        <th class="c-table-header__text">Plaats</th>
                        <th class="c-table-header__text">Naam</th>
                        <th class="c-table-header__text">Score</th>
                    </tr>`;

        for(var i = 0; i < this.length; i++) {
            if(i < 3) {
                this.htmlString += ` <tr class="c-table-row c-talbe-row-${i+1}">
                                    <td class="c-table-row-text">${i+1}</td>
                                    <td class="c-table-row-text">${this.data[i].name}</td>
                                    <td class="c-table-row-text">${this.data[i].score + this.prefix}</td>
                                </tr>`
            } else {
                this.htmlString += ` <tr class="c-table-row">
                                    <td class="c-table-row-text">${i+1}</td>
                                    <td class="c-table-row-text">${this.data[i].name}</td>
                                    <td class="c-table-row-text">${this.data[i].score + this.prefix}</td>
                                </tr>`
            }
        }

    

        this.container.innerHTML = this.htmlString;
    }

    filterLeaderboard(filter) {
        this.htmlString = `  <tr class="c-table-header">
                        <th class="c-table-header__text">Plaats</th>
                        <th class="c-table-header__text">Naam</th>
                        <th class="c-table-header__text">Score</th>
                    </tr>`;

        filter = filter.toUpperCase();

        if(!isEmpty(filter)) {
            filterArray = []
            for(var i = 0; i < this.data.length; i++) {
                if(this.data[i].name.toUpperCase().search(filter) > -1) filterArray.push({'pos': i+1, 'data': this.data[i]})
            }

            console.log(this.data.length)

            for(const f of filterArray) {
                if(f.pos < 4) {
                    this.htmlString += ` <tr class="c-table-row c-talbe-row-${f.pos}">
                                        <td class="c-table-row-text">${f.pos}</td>
                                        <td class="c-table-row-text">${f.data.name}</td>
                                        <td class="c-table-row-text">${f.data.score + this.prefix}</td>
                                    </tr>`
                } else {
                    this.htmlString += ` <tr class="c-table-row">
                                        <td class="c-table-row-text">${f.pos}</td>
                                        <td class="c-table-row-text">${f.data.name}</td>
                                        <td class="c-table-row-text">${f.data.score + this.prefix}</td>
                                    </tr>`
                }
            }
        } else {
            this.htmlString = ``
            this.loadLeaderboardHTML();
        }

        this.container.innerHTML = this.htmlString;
    }
}

// const loadLeaderboard = async (leaderboard, game, length=null, filter=null) => {
//     const data = await fetch(
//             `http://${lanIP}/tiktem/v1/leaderboard/${game}`
//         )
//         .then((r) => r.json())
//         .catch((err) => console.error("An error occurd", err));
//     // console.log(data);
//     loadLeaderboardHTML(leaderboard, data, length, filter);
// }

// const filterLeaderboard = (filter) => {
//     if(!isEmpty(filter)) {
//         filterArray = []
//         for(const d of data) {
//             if(d.name.search(filter) > -1)filterArray.push(d)
//         }
//         console.log(filterArray)
//     }
// }

// const loadLeaderboardHTML = (leaderboard, data, length=null, filter=null) => {
//     if(length==null) length=data.length;

//     data[0].scortype="t"?prefix="s":prefix=""

//     console.log(filter)

//     htmlString = `  <tr class="c-table-header">
//                         <th class="c-table-header__text">Plaats</th>
//                         <th class="c-table-header__text">Naam</th>
//                         <th class="c-table-header__text">Score</th>
//                     </tr>`;

//     if(!isEmpty(filter)) {
//         filterArray = []
//         for(const d of data) {
//             if(d.name.search(filter) > -1)filterArray.push(d)
//         }
//         console.log(filterArray)
        
//     } else {
//         for(var i = 0; i < length; i++) {
//             if(i < 3) {
//                 htmlString += ` <tr class="c-table-row c-talbe-row-${i+1}">
//                                     <td class="c-table-row-text">${i+1}</td>
//                                     <td class="c-table-row-text">${data[i].name}</td>
//                                     <td class="c-table-row-text">${data[i].score + prefix}</td>
//                                 </tr>`
//             } else {
//                 htmlString += ` <tr class="c-table-row">
//                                     <td class="c-table-row-text">${i+1}</td>
//                                     <td class="c-table-row-text">${data[i].name}</td>
//                                     <td class="c-table-row-text">${data[i].score + prefix}</td>
//                                 </tr>`
//             }
//         }
//     }
    
//     leaderboard.innerHTML = htmlString;
// }

const isEmpty = function (fieldValue) {
    return !fieldValue || !fieldValue.length;
};
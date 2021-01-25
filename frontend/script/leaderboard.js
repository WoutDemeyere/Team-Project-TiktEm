var filterArray = [];

class Leaderboard {
    constructor(leaderBoardContainer, game, length=null, ) {
        this.container = leaderBoardContainer
        this.game = game
        this.data = 0
        this.length = length
        this.htmlString = ``
        this.prefix = ""
    }

    async loadLeaderboardData(highlightname=null) {

        this.data = await fetch(
            `http://${lanIP}/tiktem/v1/leaderboard/${gamemodeInfo[this.game].id}`
        )
        .then((r) => r.json())
        .catch((err) => console.error('An err ocurd'));

        //console.log(this.data);
        highlightname==null?this.loadLeaderboardHTML():this.highlightName(highlightname)
    }

    loadLeaderboardHTML() {
        if(!this.length)this.length=this.data.length;

        this.data[0].scoretype=="t"?this.prefix="s":this.prefix=""

        if(this.data.length<this.length)this.length=this.data.length;

        // console.log(this.container)

        this.htmlString = `  <tr class="c-table-header">
                        <th class="c-table-header__text">Plaats</th>
                        <th class="c-table-header__text">Naam</th>
                        <th class="c-table-header__text">Score</th>
                    </tr>`;

        console.log(this.length)
        for(var i = 0; i < this.length; i++) {
            console.log(i)
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

    highlightName(name) {
        console.log("data")
        console.log(this.data)
        var highlight = 0
        for(var i = 0; i < this.data.length; i++) {
            if(this.data[i].name==name)highlight={'pos':i, 'item': this.data[i]};
        }

        console.log(highlight)

        this.htmlString = `  <tr class="c-table-header">
                        <th class="c-table-header__text">Plaats</th>
                        <th class="c-table-header__text">Naam</th>
                        <th class="c-table-header__text">Score</th>
                    </tr>`;

        
        for(var i = 0; i < 5; i++) {

           

            if(i < 4) {

                if(highlight.pos == i) {
                    this.htmlString += ` <tr class="c-table-row c-table-row-highlight">
                                            <td class="c-table-row-text">${highlight.pos+1}</td>
                                            <td><hr class="c-table-row-highligh-line"></td>
                                            <td class="c-table-row-text">${highlight.item.name}</td>
                                            <td><hr class="c-table-row-highligh-line"></td>
                                            <td class="c-table-row-text">${highlight.item.score}</td>
                                        </tr>`
                } else {
                    this.htmlString += ` <tr class="c-table-row c-talbe-row-${i+1}">
                                    <td class="c-table-row-text">${i+1}</td>
                                    <td class="c-table-row-text">${this.data[i].name}</td>
                                    <td class="c-table-row-text">${this.data[i].score + this.prefix}</td>
                                </tr>`
                }
                
            } else if(highlight.pos >= 4) {
                    this.htmlString += ` <tr class="c-table-row c-table-row-highlight">
                                            <td class="c-table-row-text">${highlight.pos+1}</td>
                                            <td><hr class="c-table-row-highligh-line"></td>
                                            <td class="c-table-row-text">${highlight.item.name}</td>
                                            <td><hr class="c-table-row-highligh-line"></td>
                                            <td class="c-table-row-text">${highlight.item.score}</td>
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

    showError() {
        console.log("Erreur")
        this.htmlString = ` <tr class="c-table-row c-table-row--message-container"> 
                                <td class="c-table-row--error">There is something wrong with the server</td>      
                            </tr>`
        this.container.innerHTML = this.htmlString
    }

    
}

const isEmpty = function (fieldValue) {
    return !fieldValue || !fieldValue.length;
};
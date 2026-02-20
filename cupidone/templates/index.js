class ChecklistItem {
    constructor(name, state) {
        this.name = name;
        this.state = state;
    }
}

class Card {
    constructor(id, name, description, state, checklistName, checklist, types, createdAt) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.state = state;
        this.checklistName = checklistName;
        this.checklist = checklist;
        this.types = types;
        this.createdAt = createdAt;
    }
}

const makeCardFromDict = source => {
    const checklist = [];
    for (const item of source["checklist"]) {
        checklist.push(new ChecklistItem(item["name"], item["state"]));
    }
    return new Card(
        source["id"],
        source["name"],
        source["description"],
        source["state"],
        source["checklist_name"],
        checklist,
        source["types"],
        source["created_at"]
    );
}

class CardState {
    static BACKLOG = "backlog";
    static TODO = "to do";
    static INPROGRESS = "in progress";
    static DONE = "done";
    static OUTDATED = "outdated";
}

const cardStateEmojiesMap = {
    [CardState.BACKLOG]: "🔵",
    [CardState.TODO]: "⚪",
    [CardState.INPROGRESS]: "🟡",
    [CardState.DONE]: "🟢",
    [CardState.OUTDATED]: "⭕"
}

class ChecklistItemState {
    static INCOMPLETE = "incomplete";
    static COMPLETE = "complete";
}

const checklistStateEmojiesMap = {
    [ChecklistItemState.INCOMPLETE]: "⚪",
    [ChecklistItemState.COMPLETE]: "🟢",
}

window.addEventListener("load", async () => {
    const $rootElement = document.documentElement;
    const $modal = document.getElementById("modal-one");

    const openModal = (cardId) => {
        const card = cards.find(({ id }) => id === cardId);
        $modal.querySelector("#modal-name").innerHTML = card.name;
        $modal.querySelector("#modal-created-at").innerHTML = card.createdAt;
        $modal.querySelector("#modal-type").innerHTML = card.types.map(p => `<span>${p}</span>`).join(", ");
        $modal.querySelector("#modal-state").innerHTML = `${cardStateEmojiesMap[card.state]} ${card.state}`;
        $modal.querySelector("div.description").innerHTML = card.description.map(p => `<p>${p}</p>`).join("");
        if (card.checklistName) {
            $modal.querySelector("#modal-checklist-name").removeAttribute("hidden");
            $modal.querySelector("#modal-checklist-name").innerHTML = card.checklistName;
            $modal.querySelector("#modal-checklist-items").innerHTML = card.checklist.map(item => `<div>${checklistStateEmojiesMap[item.state]} ${item.name}</div>`).join("");
        } else {
            $modal.querySelector("#modal-checklist-name").setAttribute("hidden", "");
            $modal.querySelector("#modal-checklist-name").innerHTML = "";
            $modal.querySelector("#modal-checklist-items").innerHTML = "empty";
        }
        $modal.classList.add("open");
        const exits = $modal.querySelectorAll(".modal-exit");
        exits.forEach(function (exit) {
            exit.addEventListener("click", function (event) {
                event.preventDefault();
                $modal.classList.remove("open");
            });
        });
    };

    const onCardClick = function (event) {
        event.preventDefault();
        const cardIdValue = event.target.getAttribute("data-card-id");
        const cardId = parseInt(cardIdValue);
        openModal(cardId);
    };

    const columnsMap = {};

    document.querySelectorAll("div.column").forEach(function (column) {
        const solumnState = column.getAttribute("data-column-state");
        columnsMap[solumnState] = column;
    });

    const response = await fetch("data.json");
    const data = await response.json();
    document.title = data.title;
    document.querySelector("#title").innerHTML = data.title;
    document.querySelector("#build").innerHTML = `build ${data.build}`;
    const cards = data.cards.map(makeCardFromDict);

    cards.forEach((card) => {
        const cardText = document.createTextNode(`${cardStateEmojiesMap[card.state]} ${card.name}`);
        const cardFace = document.createElement("div");
        cardFace.setAttribute("data-card-id", card.id);
        cardFace.classList.add("card");
        cardFace.appendChild(cardText);
        cardFace.addEventListener("click", onCardClick);
        columnsMap[card.state].appendChild(cardFace);
    })
});
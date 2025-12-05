let bil = [
    {
        merke: "Toyota",
        modell: "Corolla",
        år: 2020,
        farge: ["Rød", "Blå", "Svart", "Hvit", "Sølv"],
        land: "Japan"  
    },   
    {
        merke: "Ford",
        modell: "Mustang",
        år: 2019,
        farge: ["Blå", "Rød", "Gul", "Svart", "Grønn"],
        land: "USA"  
    },     
    {
        merke: "Volkswagen",
        modell: "Golf",
        år: 2018,
        farge: ["Svart", "Hvit", "Grå", "Blå", "Rød"],
        land: "Tyskland" 
    }, 
    {
        merke: "Hyundai",
        modell: "i30",
        år: 2021,
        farge: ["Hvit", "Sølv", "Svart", "Grå", "Blå"],
        land: "Sør-Korea" 
    },
    {
        merke: "Renault",
        modell: "Clio",
        år: 2017,
        farge: ["Grønn", "Rød", "Hvit", "Blå", "Gul"], 
        land: "Frankrike" 
    }
];

for (let i = 0; i < bil.length; i++) {
    console.log(bil[i].merke + " kommer fra " + bil[i].land);
}

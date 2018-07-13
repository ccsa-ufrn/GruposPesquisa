use grupospesquisa;

print("Inserindo notícias...");
EXAMPLE_ID = db.researchGroups.findOne({'name': 'Grupo+Exemplo'})._id;
EXAMPLE2_ID = db.researchGroups.findOne({'name': 'Grupo+Exemploo'})._id;
db.news.insertMany([
    {
        'ownerProgram': EXAMPLE_ID,
        'news' : [
          {
            'title': 'Lorem ipsum',
            'id': '1',
            'headline' : 'quod consequatur ex culpa labore tenetur voluptatem qui consequatur aut ut voluptas sapiente similique recusandae nemo quis qui et cumque',
            'body' : 'Atque veniam fuga magnam culpa necessitatibus. Consequatur dolorem magnam aut quod repellat temporibus vel natus. Possimus et est possimus aut ad est atque qui. Corrupti recusandae veritatis quia sed totam aspernatur qui. Esse aliquam magni ullam culpa possimus consequuntur. Dolores sint optio velit harum maiores ut. Rerum corrupti perspiciatis ipsa velit nisi saepe. Ex nostrum qui culpa. Voluptatibus molestiae ab mollitia reprehenderit. consectetur ex.'
          }
        ]
    },
    {
        'ownerProgram': EXAMPLE2_ID,
        'news': [],
    }
]);

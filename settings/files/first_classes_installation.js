use posgrad;

print("Inserindo turmas...");
PPGP_ID = db.postGraduations.findOne({'initials': 'PPGP'})._id;
PPGA_ID = db.postGraduations.findOne({'initials': 'PPGA'})._id;
PPGCC_ID = db.postGraduations.findOne({'initials': 'PPGCC'})._id;
PPGD_ID = db.postGraduations.findOne({'initials': 'PPGD'})._id;
PPGECO_ID = db.postGraduations.findOne({'initials': 'PPGECO'})._id;
PPGIC_ID = db.postGraduations.findOne({'initials': 'PPGIC'})._id;
PPGSS_ID = db.postGraduations.findOne({'initials': 'PPGSS'})._id;
PPGTUR_ID = db.postGraduations.findOne({'initials': 'PPGTUR'})._id;
db.first_classes.insertMany([
    {
        'ownerProgram': PPGP_ID,
        'first_classes'     
    },
    {
        'ownerProgram': PPGA_ID,
        'first_classes': [],
    },
    {
        'ownerProgram': PPGCC_ID,
        'first_classes': [],
    },
    {
        'ownerProgram': PPGD_ID,
        'first_classes': [],
    },
    {
        'ownerProgram': PPGECO_ID,
        'first_classes': [],
    },
    {
        'ownerProgram': PPGIC_ID,
        'first_classes': [],
    },
    {
        'ownerProgram': PPGSS_ID,
        'first_classes': [],
    },
    {
        'ownerProgram': PPGTUR_ID,
        'first_classes': [],
    }
]);

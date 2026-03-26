CREATE TABLE Organisme(
   SIRET VARCHAR2(20),  
   raison_Sociale VARCHAR2(50) ,
   PRIMARY KEY(SIRET)
);

CREATE TABLE territoire(
   IdT NUMBER(10),
   nom_territoire VARCHAR2(50) ,
   PRIMARY KEY(IdT)
);

CREATE TABLE Repas(
   IdR NUMBER(10),
   nom_repas VARCHAR2(50)  NOT NULL,
   Date_ DATE NOT NULL,
   adr_repas VARCHAR2(70) ,
   Nom_Chevalier_Dame VARCHAR2(50)  NOT NULL,
   PRIMARY KEY(IdR)
);

CREATE TABLE grade(
   IdGr NUMBER(10),
   libelle VARCHAR2(50) ,
   PRIMARY KEY(IdGr)
);

CREATE TABLE Titre(
   IdTi NUMBER(10),
   libelle VARCHAR2(50) ,
   PRIMARY KEY(IdTi)
);

CREATE TABLE Dignité(
   IdD NUMBER(10),
   libelle VARCHAR2(50) ,
   PRIMARY KEY(IdD)
);

CREATE TABLE rang(
   IdRa NUMBER(10),
   libelle VARCHAR2(50) ,
   PRIMARY KEY(IdRa)
);

CREATE TABLE composant(
   IdC NUMBER(10),
   type_aliment VARCHAR2(50) ,
   nom VARCHAR2(50) ,
   allergène VARCHAR2(50) ,
   PRIMARY KEY(IdC)
);


CREATE TABLE Légume(
   IdL NUMBER(10),
   Vérifié NUMBER(1),
   nom VARCHAR2(50) ,
   PRIMARY KEY(IdL)
);

CREATE TABLE machine(
   IdM NUMBER(10),
   nom VARCHAR2(50) ,
   PRIMARY KEY(IdM)
);

CREATE TABLE modèle(
   IdMo NUMBER(10),
   nom_modèle VARCHAR2(50) ,
   PRIMARY KEY(IdMo)
);

CREATE TABLE date_(
   date_ VARCHAR2(50) ,
   PRIMARY KEY(date_)
);
CREATE TABLE Groupe(
   IdG NUMBER(10),
   IdR NUMBER(10) NOT NULL,
   PRIMARY KEY(IdG),
   UNIQUE(IdR),
   FOREIGN KEY(IdR) REFERENCES Repas(IdR)
);

CREATE TABLE Membre(
   CodeMembre VARCHAR2(50) ,
   nom_Membre CLOB NOT NULL,
   adresse VARCHAR2(50)  NOT NULL,
   courriel VARCHAR2(50)  NOT NULL,
   num_tel VARCHAR2(50)  NOT NULL,
   IdD NUMBER(10),
   IdTi NUMBER(10),
   IdRa NUMBER(10),
   IdGr NUMBER(10) NOT NULL,
   IdG NUMBER(10),
   PRIMARY KEY(CodeMembre),
   FOREIGN KEY(IdG) REFERENCES Groupe(IdG),
   FOREIGN KEY(IdD) REFERENCES Dignité(IdD),
   FOREIGN KEY(IdTi) REFERENCES Titre(IdTi),
   FOREIGN KEY(IdRa) REFERENCES rang(IdRa),
   FOREIGN KEY(IdGr) REFERENCES grade(IdGr)
);

CREATE TABLE organisation(
   IdO NUMBER(10),
   nom_orga VARCHAR2(50)  NOT NULL,
   type_orga VARCHAR2(50)  NOT NULL,
   IdT NUMBER(10) NOT NULL,
   PRIMARY KEY(IdO),
   FOREIGN KEY(IdT) REFERENCES territoire(IdT)
);


CREATE TABLE plat(
   IdP NUMBER(10),
   IdL NUMBER(10),
   Nom_Plat VARCHAR2(20),
   PRIMARY KEY(IdP),
   FOREIGN KEY(IdL) REFERENCES Légume(IdL)
);

CREATE TABLE Entretien(
   IdE NUMBER(10),
   Certificat_d_entretien TIMESTAMP,
   CodeMembre VARCHAR2(50)  NOT NULL,
   PRIMARY KEY(IdE),
   UNIQUE(CodeMembre),
   FOREIGN KEY(CodeMembre) REFERENCES Membre(CodeMembre)
);

CREATE TABLE Ordre(
   IdO NUMBER(10),
   PRIMARY KEY(IdO),
   FOREIGN KEY(IdO) REFERENCES organisation(IdO)
);

CREATE TABLE Club(
   IdO_1 NUMBER(10),
   IdO NUMBER(10) NOT NULL,
   PRIMARY KEY(IdO_1),
   FOREIGN KEY(IdO_1) REFERENCES organisation(IdO),
   FOREIGN KEY(IdO) REFERENCES Ordre(IdO)
);

CREATE TABLE est_affilié(
   CodeMembre VARCHAR2(50),
   SIRET VARCHAR2(20),  -- 👈 C'EST CETTE LIGNE QU'IL FAUT CORRIGER
   PRIMARY KEY(CodeMembre, SIRET),
   FOREIGN KEY(CodeMembre) REFERENCES Membre(CodeMembre),
   FOREIGN KEY(SIRET) REFERENCES Organisme(SIRET)
);

CREATE TABLE adhère(
   CodeMembre VARCHAR2(50) ,
   IdO NUMBER(10),
   PRIMARY KEY(CodeMembre, IdO),
   FOREIGN KEY(CodeMembre) REFERENCES Membre(CodeMembre),
   FOREIGN KEY(IdO) REFERENCES organisation(IdO)
);

CREATE TABLE Appartient(
   CodeMembre VARCHAR2(50) ,
   IdG NUMBER(10),
   PRIMARY KEY(CodeMembre, IdG),
   FOREIGN KEY(CodeMembre) REFERENCES Membre(CodeMembre),
   FOREIGN KEY(IdG) REFERENCES Groupe(IdG)
);

CREATE TABLE contient(
   IdR NUMBER(10),
   IdP NUMBER(10),
   PRIMARY KEY(IdR, IdP),
   FOREIGN KEY(IdR) REFERENCES Repas(IdR),
   FOREIGN KEY(IdP) REFERENCES plat(IdP)
);

CREATE TABLE Est_organisé(
   CodeMembre VARCHAR2(50) ,
   IdR NUMBER(10),
   PRIMARY KEY(CodeMembre, IdR),
   FOREIGN KEY(CodeMembre) REFERENCES Membre(CodeMembre),
   FOREIGN KEY(IdR) REFERENCES Repas(IdR)
);

CREATE TABLE est_composé(
   IdP NUMBER(10),
   IdC NUMBER(10),
   PRIMARY KEY(IdP, IdC),
   FOREIGN KEY(IdP) REFERENCES plat(IdP),
   FOREIGN KEY(IdC) REFERENCES composant(IdC)
);



CREATE TABLE Est(
   IdM NUMBER(10),
   IdMo NUMBER(10),
   PRIMARY KEY(IdM, IdMo),
   FOREIGN KEY(IdM) REFERENCES machine(IdM),
   FOREIGN KEY(IdMo) REFERENCES modèle(IdMo)
);

CREATE TABLE Historique_entretien(
   IdO NUMBER(10),
   IdM NUMBER(10),
   IdE NUMBER(10),
   date_ VARCHAR2(50) ,
   PRIMARY KEY(IdO, IdM, IdE, date_),
   FOREIGN KEY(IdO) REFERENCES organisation(IdO),
   FOREIGN KEY(IdM) REFERENCES machine(IdM),
   FOREIGN KEY(IdE) REFERENCES Entretien(IdE),
   FOREIGN KEY(date_) REFERENCES date_(date_)
);

CREATE TABLE Participe(
   IdR NUMBER(10),
   IdM NUMBER(10),
   PRIMARY KEY(IdR, IdM),
   FOREIGN KEY(IdR) REFERENCES Repas(IdR),
   FOREIGN KEY(IdM) REFERENCES machine(IdM)
);

CREATE TABLE Effectue(
   IdM NUMBER(10),
   IdE NUMBER(10),
   PRIMARY KEY(IdM, IdE),
   FOREIGN KEY(IdM) REFERENCES machine(IdM),
   FOREIGN KEY(IdE) REFERENCES Entretien(IdE)
);

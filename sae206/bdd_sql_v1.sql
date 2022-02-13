SET FOREIGN_KEY_CHECKS=0;

-- ------------------------------------------------------------------UTILISATEUR-----------------------------------------------------------------
DROP TABLE IF EXISTS UTILISATEUR;

CREATE TABLE UTILISATEUR(
   id_user INT AUTO_INCREMENT,
   email VARCHAR(255),
   username VARCHAR(50),
   password VARCHAR(255),
   role VARCHAR(255),
   est_actif INT,   -- 0 pour non, 1 pour oui
   PRIMARY KEY(id_user)
);

INSERT INTO UTILISATEUR(id_user, email, username, password, role, est_actif) VALUES
(NULL, 'admin@admin.fr', 'admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1),
(NULL, 'client@client.fr', 'client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1),
(NULL, 'client2@client2.fr', 'client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client',1);

SELECT * FROM UTILISATEUR;


-- -------------------------------------------------------------------TYPE_VELO------------------------------------------------------------------
DROP TABLE IF EXISTS TYPE_VELO;

CREATE TABLE TYPE_VELO(
   id_type_velo INT AUTO_INCREMENT,
   libelle_type_velo VARCHAR(50),
   PRIMARY KEY(id_type_velo)
);

INSERT INTO TYPE_VELO(libelle_type_velo) VALUES
('VTT'),('Vélo de route'),('Vélo de ville'),
('Vélo Tout Chemin'),('Vélo pliant');

SELECT * FROM TYPE_VELO;


-- ---------------------------------------------------------------------TAILLE-------------------------------------------------------------------
DROP TABLE IF EXISTS TAILLE;

CREATE TABLE TAILLE(
   id_taille INT AUTO_INCREMENT,
   libelle_taille VARCHAR(50),
   PRIMARY KEY(id_taille)
);

INSERT INTO TAILLE(libelle_taille)
VALUES ('S'),('M'),('L'),('XL'),('XXL');

SELECT * FROM TAILLE;


-- --------------------------------------------------------------------COULEUR-------------------------------------------------------------------
DROP TABLE IF EXISTS COULEUR;

CREATE TABLE COULEUR(
   id_couleur INT AUTO_INCREMENT,
   libelle_couleur VARCHAR(50),
   PRIMARY KEY(id_couleur)
);

INSERT INTO COULEUR(libelle_couleur) VALUES
('Rouge'),('Orange'),('Jaune'),('Vert'),('Bleu'),('Bleu Foncé'),('Blanc'),('Gris'),('Gris Foncé'),('Noir');


-- -------------------------------------------------------------------FOURNISSEUR-----------------------------------------------------------------
DROP TABLE IF EXISTS FOURNISSEUR;

CREATE TABLE FOURNISSEUR(
   id_fournisseur INT AUTO_INCREMENT,
   nom_fournisseur VARCHAR(50),
   adresse_fournisseur VARCHAR(255),
   num_tel_fournisseur VARCHAR(15),
   PRIMARY KEY(id_fournisseur)
);

INSERT INTO FOURNISSEUR(nom_fournisseur, adresse_fournisseur, num_tel_fournisseur) VALUES
('Cycles Lapierre','Rue Edmond Voisenet, 21000 DIJON','080019462121'),
('Scott France','25 rue Topaze, ZA Les Jalassières, 13510 AIGUILLES','0892977107'),
('Shimano France','777 rue Commios, 62223 SAINT-LAURENT-BLANGY','0890109232'),              -- Pour certaines pièces
('Trek Bicycle Toulouse Ouest','35 bis Route de Toulouse, 31700 Cornebarrieu','0532780399'),
('Decathlon','Zonne Commerciale Porte des Vosges 90160 BESSONCOURT','0384285418'),
('Specialized Europe BV','Chemin de Presles, 07800 CHARMES-SUR-RHÔNE', NULL);       -- Nouvelle adresse introuvable depuis un incendie l'an passé

SELECT * FROM FOURNISSEUR;

-- ----------------------------------------------------------------------ETAT--------------------------------------------------------------------
DROP TABLE IF EXISTS ETAT;

CREATE TABLE ETAT(
   id_etat INT AUTO_INCREMENT,
   libelle_etat VARCHAR(255),
   PRIMARY KEY(id_etat)
);

INSERT INTO ETAT(libelle_etat) VALUES
('En cours de traîtement'),('Expédié'),('Validé');

SELECT * FROM ETAT;

-- ----------------------------------------------------------------------VELO--------------------------------------------------------------------
DROP TABLE IF EXISTS VELO;

CREATE TABLE VELO(
   id_velo INT AUTO_INCREMENT,
   nom_velo VARCHAR(255),
   id_type_velo INT NOT NULL,
   id_taille INT NOT NULL,
   id_couleur INT NOT NULL,
   prix_velo NUMERIC(7,2),
   stock INT,
   img_velo VARCHAR(255),
   PRIMARY KEY(id_velo),
   CONSTRAINT fk_type_velo
        FOREIGN KEY(id_type_velo)
        REFERENCES TYPE_VELO(id_type_velo),

   CONSTRAINT fk_taille_velo
        FOREIGN KEY(id_taille)
        REFERENCES TAILLE(id_taille),

   CONSTRAINT fk_couleur_velo
        FOREIGN KEY(id_couleur)
        REFERENCES COULEUR(id_couleur)
);

INSERT INTO VELO(nom_velo, id_type_velo, id_taille, id_couleur, prix_velo, stock, img_velo) VALUES
('Trek EMONDA SL 5 DISC',2,4,6,2999,1000,'emonda_bleu_fonce.png'),
('Lapierre Aircode DRS 6.0',2,3,7,4399,880,'aircode_drs_blanc.png'),
('Scott Scale 910 AXS',1,2,8,3699,455,'scale_910_axs.png'),
('Elops 920 Cadre Bas',3,3,7,1399,1715,'elops_920.png'),
('Rockrider ST 530 Jaune',1,2,3,429,401,'rockrider_st530.png'),
('Riverside 920',4,3,10,769,850,'riverside920.png'),
('Oxylane 120 Rouge',5,3,1,269,1300,'oxylane_120_rouge.png'),
('Specialized Diverge Elite E5',2,3,3,2100,305,'diverge_elite_e5_jaune.png'),
('S-Works Roubaix SRAM Red eTAP AXS',2,3,4,12000,150,'roubaix_red_etap_axs.png');

SELECT * FROM VELO;

-- --------------------------------------------------------------------COMMANDE------------------------------------------------------------------
DROP TABLE IF EXISTS COMMANDE;

CREATE TABLE COMMANDE(
   id_commande INT NOT NULL AUTO_INCREMENT,
   date_achat DATETIME,
   id_user INT,
   id_etat INT,
   prix_total INT,
   PRIMARY KEY(id_commande),

   CONSTRAINT fk_commande_user
        FOREIGN KEY(id_user)
        REFERENCES UTILISATEUR(id_user),

   CONSTRAINT fk_commande_etat
        FOREIGN KEY(id_etat)
        REFERENCES ETAT(id_etat)
);

-- ---------------------------------------------------------------------PANIER-------------------------------------------------------------------
DROP TABLE IF EXISTS PANIER;

CREATE TABLE PANIER(
   id_panier INT AUTO_INCREMENT,
   date_ajout DATE,
   prix_unit INT,
   quantite INT,
   id_velo INT NOT NULL,
   id_user INT NOT NULL,
   PRIMARY KEY(id_panier),

   CONSTRAINT fk_panier_velo
        FOREIGN KEY(id_velo)
        REFERENCES VELO(id_velo),

   CONSTRAINT fk_panier_user
        FOREIGN KEY(id_user)
        REFERENCES UTILISATEUR(id_user)
);


-- -----------------------------------------------------------------ligne_commande---------------------------------------------------------------
DROP TABLE IF EXISTS ligne_commande;

CREATE TABLE ligne_commande(
    id_ligne INT NOT NULL AUTO_INCREMENT,
    id_velo INT,
    id_commande INT,
    prix_unit INT,
    quantite INT,
    PRIMARY KEY(id_ligne),
    CONSTRAINT fk_ligne_comm_velo
        FOREIGN KEY(id_velo)
        REFERENCES VELO(id_velo),

    CONSTRAINT fk_ligne_comm_commande
        FOREIGN KEY(id_commande)
        REFERENCES COMMANDE(id_commande)
);


-- --------------------------------------------------------------------fabrique------------------------------------------------------------------
DROP TABLE IF EXISTS fabrique;

CREATE TABLE fabrique(
   id_velo INT,
   id_fournisseur INT,
   PRIMARY KEY(id_velo, id_fournisseur),
   CONSTRAINT fk_fabrique_velo
       FOREIGN KEY(id_velo)
       REFERENCES VELO(id_velo),

   CONSTRAINT fk_fabrique_fournisseur
       FOREIGN KEY(id_fournisseur)
       REFERENCES FOURNISSEUR(id_fournisseur)
);

INSERT INTO fabrique VALUES
(1,4),(2,1),(3,2),
(4,5),(5,5),(6,5),(7,5),
(8,6),(9,6);

SELECT * FROM fabrique;


-- Test de jointure
SELECT VELO.id_velo, nom_velo,
       CONCAT(TYPE_VELO.libelle_type_velo,' (',VELO.id_type_velo,')') AS type_velo,
       CONCAT(TAILLE.libelle_taille,' (',VELO.id_taille,')') AS taille,
       CONCAT(COULEUR.libelle_couleur,' (',VELO.id_couleur,')') AS couleur,
       CONCAT(FOURNISSEUR.nom_fournisseur,' (',FOURNISSEUR.id_fournisseur,')') AS fournisseur,
       prix_velo, stock, img_velo
FROM VELO
INNER JOIN TYPE_VELO ON VELO.id_type_velo = TYPE_VELO.id_type_velo
INNER JOIN TAILLE ON VELO.id_taille = TAILLE.id_taille
INNER JOIN COULEUR on VELO.id_couleur = COULEUR.id_couleur
INNER JOIN fabrique ON VELO.id_velo = fabrique.id_velo
INNER JOIN FOURNISSEUR ON fabrique.id_fournisseur = FOURNISSEUR.id_fournisseur
ORDER BY id_velo;

-- Supression des clés étrangères
ALTER TABLE fabrique
    DROP FOREIGN KEY fk_fabrique_velo;
ALTER TABLE fabrique
    DROP FOREIGN KEY fk_fabrique_fournisseur;

ALTER TABLE ligne_commande
    DROP FOREIGN KEY fk_ligne_comm_velo;
ALTER TABLE ligne_commande
    DROP FOREIGN KEY fk_ligne_comm_commande;

ALTER TABLE PANIER
    DROP FOREIGN KEY fk_panier_velo;
ALTER TABLE PANIER
    DROP FOREIGN KEY fk_panier_user;

ALTER TABLE COMMANDE
    DROP FOREIGN KEY fk_commande_user;
ALTER TABLE COMMANDE
    DROP FOREIGN KEY fk_commande_etat;

ALTER TABLE VELO
    DROP FOREIGN KEY fk_couleur_velo;
ALTER TABLE VELO
    DROP FOREIGN KEY fk_type_velo;
ALTER TABLE VELO
    DROP FOREIGN KEY fk_taille_velo;
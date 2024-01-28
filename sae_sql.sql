-- Suppression des tables si elles existe
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS parfum;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS volume;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS utilisateur;

-- Création de la table utilisateur
CREATE TABLE utilisateur(
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(255),
    nom VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    est_actif tinyint(1),
    PRIMARY KEY (id_utilisateur)
)DEFAULT CHARSET utf8mb4;

-- Création de la table genre
CREATE TABLE genre(
                      id_genre INT AUTO_INCREMENT,
                      nom_genre VARCHAR(255),
                      PRIMARY KEY(id_genre)
)DEFAULT CHARSET utf8mb4;

-- Création de la table volume
CREATE TABLE volume(
                       id_volume INT AUTO_INCREMENT,
                       nom_volume VARCHAR(255),
                       PRIMARY KEY(id_volume)
)DEFAULT CHARSET utf8mb4;

-- Création de la table etat
CREATE TABLE etat(
                     id_etat INT AUTO_INCREMENT,
                     libelle VARCHAR(255),
                     PRIMARY KEY(id_etat)
)DEFAULT CHARSET utf8mb4;

-- Création de la table commande
CREATE TABLE commande(
                         id_commande INT AUTO_INCREMENT,
                         date_achat DATE,
                         utilisateur_id INT,
                         etat_id INT,
                         PRIMARY KEY(id_commande),
                         FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                         FOREIGN KEY(etat_id) REFERENCES etat(id_etat)
)DEFAULT CHARSET utf8mb4;


-- Création de la table parfum
CREATE TABLE parfum(
    id_parfum INT AUTO_INCREMENT,
    nom_parfum VARCHAR(255),
    prix_parfum DOUBLE,
    volume_id INT,
    type_parfum_id INT,
    conditionnement VARCHAR(255),
    description VARCHAR(255),
    fournisseur VARCHAR(255),
    marque VARCHAR(255),
    stock INT,
    image VARCHAR(255),
    PRIMARY KEY(id_parfum),
    FOREIGN KEY(volume_id) REFERENCES volume(id_volume),
    FOREIGN KEY(type_parfum_id) REFERENCES genre(id_genre)
)DEFAULT CHARSET utf8mb4;

-- Création de la table ligne_commande
CREATE TABLE ligne_commande(
                               commande_id INT ,
                               parfum_id INT ,
                               prix DOUBLE,
                               quantite INT,
                                   PRIMARY KEY(commande_id,parfum_id),
                               FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
                               FOREIGN KEY(parfum_id) REFERENCES parfum(id_parfum)
)DEFAULT CHARSET utf8mb4;

-- Création de la table ligne_panier
CREATE TABLE ligne_panier(
                             utilisateur_id INT ,
                             parfum_id INT ,
                             quantite INT,
                             date_ajout DATE,
                             PRIMARY KEY(utilisateur_id,parfum_id),
                             FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                             FOREIGN KEY(parfum_id) REFERENCES parfum(id_parfum)
)DEFAULT CHARSET utf8mb4;

-- Insertion de données dans la table utilisateur
INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
    'ROLE_client','client2','1');

-- Insertion de données dans la table volume
INSERT INTO volume(nom_volume) VALUES
('50 ml'),
('100 ml'),
('200 ml');

-- Insertion de données dans la table genre
INSERT INTO genre(nom_genre) VALUES
                                          ('femme'),
                                          ('homme'),
                                          ('mixte'),
                                          ('enfant');

-- Insertion de données dans la table etat
INSERT INTO etat(libelle) VALUES ('en attente'), ('expédié'), ('validé'), ('confirmé');

-- Insertion de données dans la table parfum
INSERT INTO parfum( nom_parfum, prix_parfum, volume_id, type_parfum_id, conditionnement, description, fournisseur, marque, stock ,image) VALUES
                    ('batman 100ml', 10.0, 2, 4, 'flacon plastique','Parfum Batma,', 'Made in Italie', 'naturaverde', 5,'batman.jpeg'),
                    ('licorne 50ml', 15.0, 1, 4,'flacon plastique', 'Parfum Licorne', 'air-val', 'netball',7,'licorne.jpg'),
                    ('spiderman 100ml', 13.0, 2, 4, 'flacon en aluminium','Parfum spiderman', 'air-val', 'marvel',10, 'spiderman.jpeg'),
                    ('Azzaro 200ml', 70.0, 3, 2, 'flacon verre','Azzaro parfum', 'Oréal Luxe Division.k', 'La Maison',6, 'azzaro-100ml.jpeg'),
                    ('Exotic Gold 200ml', 100.0, 3, 3, 'flacon verre','Parfum Exotic Gold', 'Louis Cardin', 'Louis Cardin',8, 'louiscardin.jpeg'),
                    ('One Million 50ml', 78.0, 1, 2, 'flacon en aluminium','Parfum One million', 'la maison Paco Rabanne', 'Paco Rabanne',20, 'onemillion-50ml.webp'),
                    ('Sauvage 100ml', 254.0, 2, 2, 'flacon verre','Parfum Sauvage', 'Dior', 'Dior',7, 'sauvage.jpg'),
                    ('Invictus 50ml', 78.75, 1, 2, 'flacon aluminium','Parfum Invicus', 'la maison Paco Rabanne', 'Paco Rabanne',5, 'invicus.jpg'),
                    ('Idole 100ml', 135.0, 2, 1, 'flacon verre','Parfum Idole', 'Le domaine de la Rose', 'Lancôme',4, 'idole.jpeg'),
                    ('Miss Dior 200ml', 222.0, 3, 1, 'flacon verre','Parfum miss dior', 'Dior', 'Dior',25, 'missdior.jpeg'),
                    ('Roja 50ml', 725.0, 1, 3, 'flacon verre','Roja parfum', 'aoud', 'aoud',30, 'aoud.jpeg'),
                    ('Éphémère 100ml', 25.0, 2, 4, 'flacon aluminium','Parfum “Ma petite eau éphémère” pour enfants', 'Grasse', 'Minikane',4, 'ephemere.jpeg'),
                    ('Herman 50ml', 98.0, 1, 3, 'flacon verre','HERMANN A MES COTES ME PARAISSAIT UNE OMBRE', 'Etat libre orange', 'Etat libre orange',10, 'herman.jpeg'),
                    ('tresor 100ml', 114.0, 2, 1, 'flacon verre','tresor parfum', 'Lancôme', 'Lancôme',20, 'tresor-75ml.jpeg'),
                    ('working girl 200ml', 255.0, 3, 1,'flacon verre', 'girl parfum', 'jspp', 'working',2, 'working_girl_100ml.jpeg'),
                    ('batman 50ml', 7.0, 1, 4, 'flacon plastique','Parfum Batma,', 'Made in Italie', 'naturaverde', 5,'batman-50ml.jpg'),
                    ('Azzaro 50ml', 50.0, 1, 2, 'flacon verre','Azzaro parfum', 'Oréal Luxe Division.k', 'La Maison',6, 'azzaro-50ml.jpg'),
                    ('One Million 200ml', 200.0, 3, 2, 'flacon en aluminium','Parfum One million', 'la maison Paco Rabanne', 'Paco Rabanne',20, 'onemillion-200ml.webp'),
                    ('Sauvage 50ml', 154.0, 1, 2, 'flacon verre','Parfum Sauvage', 'Dior', 'Dior',7, 'sauvage-50ml.jpg'),
                    ('Miss Dior 50ml', 222.0, 1, 1, 'flacon verre','Parfum miss dior', 'Dior', 'Dior',25, 'missdior-50ml.jpg'),
                    ('tresor 200ml', 170.0, 3, 1, 'flacon verre','tresor parfum', 'Lancôme', 'Lancôme',20, 'tresor.jpeg'),
                    ('working girl 50ml', 148.0, 1, 1,'flacon verre', 'girl parfum', 'jspp', 'working',2, 'working_girl_50ml.jpeg');

-- Insertion de données dans la table commande
INSERT INTO commande( date_achat , utilisateur_id , etat_id ) VALUES
                    ('2015-02-02', 2, 1),
                    ('2020-01-10', 3, 2),
                    ('2050-10-30', 1, 3);

-- Insertion de données dans la table ligne_commande
INSERT INTO  ligne_commande(commande_id, parfum_id, prix, quantite) VALUES
                            (1, 2, 20.0, 2),
                            (2, 5, 19.36, 3);

-- Insertion de données dans la table ligne_panier
INSERT INTO ligne_panier ( utilisateur_id, parfum_id, quantite, date_ajout) VALUES
                                                                                     (1, 3, 2, '2024-01-02'),
                                                                                     (3, 7, 1, '2023-10-30'),
                                                                                     (2, 15, 3, '2023-12-27'),
                                                                                     (1, 21, 1, '2023-11-04');

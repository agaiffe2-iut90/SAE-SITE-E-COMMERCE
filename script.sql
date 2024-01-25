DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS parfum;
DROP TABLE IF EXISTS type_parfum;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS volume;
DROP TABLE IF EXISTS utilisateur;

CREATE TABLE utilisateur(
    id_utilisateur INT AUTO_INCREMENT,
    login VARCHAR(255),
    email VARCHAR(255),
    nom VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    est_actif tinyint(1),
    PRIMARY KEY (id_utilisateur)
);

CREATE TABLE genre(
                      id_genre INT AUTO_INCREMENT,
                      nom_genre VARCHAR(255),
                      PRIMARY KEY(id_genre)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE volume(
                       id_volume INT AUTO_INCREMENT,
                       nom_volume VARCHAR(255),
                       PRIMARY KEY(id_volume)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE etat(
                     id_etat INT AUTO_INCREMENT,
                     libelle VARCHAR(255),
                     PRIMARY KEY(id_etat)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE commande(
                         id_commande INT AUTO_INCREMENT,
                         date_achat DATE,
                         utilisateur_id INT,
                         etat_id INT,
                         PRIMARY KEY(id_commande),
                         FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                         FOREIGN KEY(etat_id) REFERENCES etat(id_etat)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE type_parfum(
                       id_type_parfum INT AUTO_INCREMENT,
                       marque VARCHAR(255),
                       PRIMARY KEY(id_parfum)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE parfum(
                       id_parfum INT AUTO_INCREMENT,
                       nom_parfum VARCHAR(255),
                       prix_parfum DOUBLE,
                       volume_id INT,
                       type_parfum_id INT,
                       description VARCHAR(255),
                       fournisseur VARCHAR(255),
                       marque VARCHAR(255),
                       image VARCHAR(255),
                       PRIMARY KEY(id_parfum),
                       FOREIGN KEY(volume_id) REFERENCES volume(id_volume),
                       FOREIGN KEY(type_parfum_id) REFERENCES genre(id_genre)
)DEFAULT CHARSET utf8mb4;


CREATE TABLE ligne_commande(
                               commande_id INT ,
                               parfum_id INT ,
                               prix DOUBLE,
                               quantite INT,
                                   PRIMARY KEY(commande_id,parfum_id),
                               FOREIGN KEY(commande_id) REFERENCES commande(id_commande),
                               FOREIGN KEY(parfum_id) REFERENCES parfum(id_parfum)
)DEFAULT CHARSET utf8mb4;

CREATE TABLE ligne_panier(
                             utilisateur_id INT ,
                             parfum_id INT ,
                             quantite INT,
                             date_ajout DATE,
                             PRIMARY KEY(utilisateur_id,parfum_id),
                             FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                             FOREIGN KEY(parfum_id) REFERENCES parfum(id_parfum)
)DEFAULT CHARSET utf8mb4;

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

INSERT INTO volume(nom_volume) VALUES
('50 ml'),
('100 ml'),
('200 ml');

INSERT INTO genre(nom_genre) VALUES
                                          ('femme'),
                                          ('homme'),
                                          ('mixte'),
                                          ('enfant');

INSERT INTO etat(libelle) VALUES ('en attente'), ('expédié'), ('validé'), ('confirmé');

INSERT INTO parfum( nom_parfum, prix_parfum, volume_id, type_parfum_id, description, fournisseur, marque ,image) VALUES
                    ('batman', 30.0, 2, 4, 'batman parfum', 'italie', 'naverde', 'batman.jpeg'),
                    ('licorne', 19.0, 1, 4, 'licorne parfum', 'netball', 'air-val', 'licorne.jpeg'),
                    ('spiderman', 20.0, 2, 4, 'spiderman parfum', 'marvel', 'marvel', 'spiderman.jpeg'),
                    ('tresor', 50.0, 2, 1, 'tresor parfum', 'china', 'jsp', 'tresor.jpg'),
                    ('working girl', 255.0, 3, 1, 'girl parfum', 'jspp', 'working', 'working_girl_100ml.jpg');

INSERT INTO commande( date_achat , utilisateur_id , etat_id ) VALUES
                    ('2015-02-02', 2, 1),
                    ('2020-01-10', 3, 2),
                    ('2050-10-30', 1, 3);

INSERT INTO  ligne_commande(commande_id, parfum_id, prix, quantite) VALUES
                            (1, 2, 20.0, 2),
                            (2, 5, 19.36, 3);
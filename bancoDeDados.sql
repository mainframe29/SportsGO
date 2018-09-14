drop database sports;

create database sports;
use sports

create table usuario(
id_usu int(5) primary key auto_increment not null,
nome varchar(20),
nick varchar(20) not null,
email varchar(50),
senha longtext,
sp_Fav int(5),
pontos int(50)
);


create table seguir(
id_seguindo int(5),
id_seguidor int(5)
);

create table esportes(
id_spo int(5) primary key auto_increment not null,
nome varchar(50),
historia longtext,
regras longtext,
tipo varchar(20)
);

create table videos(
id_video int(5) primary key auto_increment not null,
titulo varchar(50),
url longtext,
legenda varchar(50),
id_usu int (5),
tag int(5)
);

create table quiz (
id_quiz int(5) primary key auto_increment not null,
pergunta varchar(255),
alternativaA varchar(255),
alternativaB varchar(255),
alternativaC varchar(255),
alternativaD varchar(255),
resposta char(1),
ponto int(4),
esporte int(5) 
);

create table missao (
id_missao int(5) primary key auto_increment not null,
titulo varchar(50),
descr varchar(100),
nivel int(4),
ponto int(5) 
);

create table usu_Missao(
id_usu int(5),
id_missao int(5),
concluido char(1)
);

create table usu_quiz(
id_usu int(5),
id_quiz int(5),
concluido char(1)
);

/* *****FOREIGN KEY de Seguir com Usuário***** */

alter table seguir add constraint pk_seguir primary key (id_seguindo, id_seguidor);
alter table seguir add constraint fk_seguindo foreign key (id_seguindo) references usuario (id_usu);
alter table seguir add constraint fk_seguidor foreign key (id_seguidor) references usuario (id_usu);

/* *****FOREIGN KEY de videos com usuario***** */
alter table videos add constraint fk_video_usu foreign key (id_usu) references usuario (id_usu);

/* *****FOREIGN KEY de videos com esporte***** */
alter table videos add constraint fk_video_esporte foreign key (tag) references esportes (id_spo);

/* *****FOREIGN KEY de usuario com esporte***** */
alter table usuario add constraint fk_usuario_esporte foreign key (sp_Fav) references esportes (id_spo);

/* *****FOREIGN KEY de quiz com esporte***** */
alter table quiz add constraint fk_quiz_esporte foreign key (esporte) references esportes (id_spo);

/* *****FOREIGN KEY de usu_Missao com usuario e missao***** */
alter table usu_Missao add constraint pk_usu_missao primary key (id_usu, id_missao);
alter table usu_Missao add constraint fk_usu_missao foreign key (id_usu) references usuario (id_usu);
alter table usu_Missao add constraint fk_missao_usu foreign key (id_missao) references missao (id_missao);

/* *****FOREIGN KEY de usu_Missao com usuario e quiz***** */
alter table usu_quiz add constraint pk_usu_quiz primary key (id_usu, id_quiz);
alter table usu_quiz add constraint fk_usu_quiz foreign key (id_usu) references usuario (id_usu);
alter table usu_quiz add constraint fk_quiz_usu foreign key (id_quiz) references quiz (id_quiz);

insert into usuario values(0, "Vini", "vini123", "vi@hotmail.com",  "oi123", 1, 0);
insert into usuario values(0, "Jami", "jamii123", "ja@hotmail.com",  "oi123", 1, 0);
insert into usuario values(0, "Karine", "kari123", "ka@hotmail.com",  "oi123", 1, 0);
insert into usuario values(0, "Le", "le123", "le@hotmail.com",  "oi123", 1, 0);

insert into esportes values (0, 'Karate', 'O Karate é uma arte marcial originada nas ilhas de RyuKyu, localizadas atualmente em Okinawa, Japão. Desenvolveu-se a partir de artes marciais indígenas recebendo influência de artes marciais chinesas. 
A popularidade do Karate, assim como de outras artes marciais, aumentou no mundo todo nas décadas de 1960 e 1970 graças aos filmes de artes marciais, estes que até hoje continuam sendo criados e se tornando grandes sucessos. 
Durante a evolução do Karate foram criados diferentes estilos, que são em tese adaptações do Karate que foi originado em Okinawa. Atualmente existem oito estilos: 
-Goju Ryu: visa buscar o equilíbrio dos opostos, das energias antagônicas e complementares, aprendendo a agir com energia, calma, rapidez e suavidade.
-Shito Ryu: é a combinação da suavidade e da versatilidade das técnicas de combate e pela inclusão de técnicas de solo.
-Shorin Ryu: é o estilo original de Okinawa, e a partir dele surgiram todos os outros.
-Shotokan: bases fortes e golpes no corpo inteiro, movimentos que se iniciam como defesa e se dominados completamente dão ao Karate-ka um golpe de força altíssima. 
-Wado Ryu: utilização de técnicas de esquiva, projeção, movimentação e troca de guarda.
-Uechi Ryu: é uma mistura com o Kung Fu e provém de três animais: garça, tigre e o dragão. O Uechi Ryu visa o equilíbrio da garça, a força do tigre e a sabedoria do dragão.
-Kenyu Tyu: tem como características, movimentos fortes circulares e de esquivas, o que torna este estilo muito técnico e complexo.
-Kyokushin Kai: é fundamentado em técnicas compactadas e eficazes que visam nocautear o oponente com um único golpe, que é aplicado com uma grande força.
No Karate existem alguns títulos, o praticante de Karate, por exemplo, é chamado de Karate–ka, tendo como professor o Sensei, este que foi treinado por quem chamamos de Mestre.
','Numa competição de estilo livre, a luta é iniciada pelo árbitro com 2 rounds de 3 minutos, neste tempo o karate-ka pode desferir qualquer golpe estando dentro dos existentes no Karate. Cada golpe acertado, é atribuído pontuações, sendo elas:
-Yuko: Qualquer soco em qualquer parte do corpo acima da cintura;
-Wazari: Chutes na região do tronco do oponente;
-Ippon: Chutes na região da cabeça e derrubadas com finalizações.', 'Arte Marcial');

insert into quiz values(0, 'Em qual país se originou o Karate?', 'a) Espanha', 'b) Brasil', 'c) Japão', 'd) China', 'c', 1, 1);
insert into quiz values(0, 'Quais eram, respectivamente, as ilhas precursoras e a ilha atual da origem do Karate?', 'a)Ilha da Páscoa, Xamarin', 'b) RyuKyu, Okinawa', 'c) Shinoku, Ishigaki', 'd) Arvoredos, Vaygach', 'b', 1, 1);
insert into quiz values(0, 'O estilo ____________  é composto por bases fortes e golpes no corpo inteiro, movimentos que se iniciam como defesa e se dominados completamente dão ao Karate-ka um golpe de força altíssima.', 'a) Goju Ryu', 'b) Kenyu Tyu', 'c) Kyokushin Kai', 'd) Shotokan', 'd', 1, 1);

insert into quiz values(0, 'Em qual país se originou o Karate?', 'a) Espanha', 'b) Brasil', 'c) Japão', 'd) China', 'c', 1, 1);
insert into quiz values(0, 'Em qual país se originou o Karate?', 'a) Espanha', 'b) Brasil', 'c) Japão', 'd) China', 'c', 1, 1);
insert into quiz values(0, 'Em qual país se originou o Karate?', 'a) Espanha', 'b) Brasil', 'c) Japão', 'd) China', 'c', 1, 1);

/*BUSCAR PERGUNTA DE TAL ESPORTE*/
select id_quiz, pergunta from quiz where esporte = 1 limit 0,0; --primeiro 0 é do deslocamento, segundo 0 é quantos registros pegará


insert into seguir values( 2, 3);

/*SEGUINDO*/
select us.nome from usuario us inner join seguir se on us.id_usu=se.id_seguidor where id_seguindo = 1;

/*SEGUIDORES*/
select us.nome from usuario us inner join seguir se on us.id_usu=se.id_seguindo where id_seguidor = 1;
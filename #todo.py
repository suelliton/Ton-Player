#todo
#0 - renomer mainview para listening_view
#1 -[listening_view, download_view] adicionar stack main e tabs para alternar entre listening_view e download_view tabs
#1.1 - melhorar apresentação da lista de albuns para download
#2 - ao carregar as músicas de uma pasta através do botão +musics, deverá já inluir os metadados do arquivo mp3, use mutagen para recupera
#3 - ao adicionar músicas vindas do "spotify", deverá ser antes criada uma playlist com o nome e arte do album, para posterior adição automática das músicas 
#3.1 - incluir coverart na lista de playlist
#4 - ao baixar um album, ao término do download deverá ser preenchida a playlist criada anteriormente do album, metadados deverão ser carregados também do arquivo .mp3
#5 - verificar se a lista de playlists contem scroll
#6 - adicionar busca por album/playlist na aba listen_view
#7 - melhorar apresentação da lista de músicas , usar como base a do spotify
#7.1 - incluir github
#8 - retirar botão de pause e stop, deixar apenas um botão play/pause e trazer o slide de volume para o mesmo alinhamento
#20 - incluir uma arte de disco rotativa para indicar que o áudio está tocando
#9 - verificar formas de avançar a música ao clicar na barra de carregamento, testar se com slider dá certo



#10- melhorar apresentação da listagem de playlist



#10.1 arranjar uma foto png para coverart playlist-default
#10.2- na função de incluir músicas manualmente, incluir uma tarefa para incluir como coverart da playlist a coverart da primeira música
#10.3- incluir as actions(...) com popupmenu na lista da musica para remover etc
#10.4- investigar bug na atualização dos segundos da musica e da progressbar e da imagem que gira
#11 -[download_view] adicionar container colapse abaixo do elemento do ambum para mostrar nomes das faixas quando clicado em um botão 
#11.1 - adicionar função de notificação em utils para ser usada com mais facilidade
#12 - adicionar snackbar de notificações quando iniciar e quando terminar de baixar um album
#12.1- adicionar notificações 
#13 - organizar em pastas os componentes, criar pasta views
#14 - ao mudar de tab os elementos que são atualizados enquanto toca o audio não são encontrados pois eles são apagados da view, verificar possibilidade de apenas trocar eles de posição no array de controls da stack_main
#15 - inluir nome do artista e album na pasta coverart para evitar conflitos de músicas com mesmo nome
#16 - adicionar campo de texto para indicar a quantidade de faixas num album na listagem para download
#17 - adicionar artista ao model playlist/album
#18 - adicionar nome do album e embaixo o nome do artista na lista de playlist/album
#19 - No drawer, analisar e retirar a rolagem do conteúdo todo, deixando apenas para a listview o scroll, deixando os outros elementos fixos
#21 - adicionar campo last_listen no model playlist/album, e ao dar player atualizar este campo para listar as playlists com os mais recentes ouvidos
#22 - criar elementos de lista que se adaptem a tela em arquivo separado e depois repassar pro software
#23 - adicionar suporte com pystray para controlar o player pela bandeja do sistema
#24 - verificar container, alinhamentos das columns e rows para deixar a altura responsiva
#25 - Apagar trechos de código comentado e salvar trechos importantes em examples

#26 - criar executável, empacotar para linux e criar um github pro projeto com github pages
#27 - Testar por várias horas

######### versão 1.1 ###########

#1- incluir popup para editar o nome da playlist nos três pontinhos de cada playlist
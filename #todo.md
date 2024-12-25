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
#10.5- incluir README.md
#10.1 arranjar uma foto png para coverart playlist-default
#10.2- na função de incluir músicas manualmente, incluir uma tarefa para incluir como coverart da playlist a coverart da primeira música
#10.3- incluir as actions(...) com popupmenu na lista da musica para remover etc
#11 -[download_view] adicionar container colapse abaixo do elemento do album para mostrar nomes das faixas quando clicado em um botão 
#10.4- investigar bug na atualização dos segundos da musica e da progressbar e da imagem que gira
#10.6 - criar interface e classe concreta de player de áudio com vlc, implementar funções fora do app e depois incluir 
#10.7 Usar primeiramente a nova classe FletPlayer e depois migrar para VlcPlayer, analisar o funcinamento e melhorias de bugs
#10.5 - investigar bug quando atualiza o self.player, modifica a lista de músicas como se atualizasse em background
#11.1 - adicionar função de notificação em commons.py para ser usada com mais facilidade
#12 - adicionar snackbar de notificações quando iniciar e quando terminar de baixar um album
#12.1- adicionar notificações quando atualizar metadados, quando salvar metadados
#12.2- Investigar porque as vezes o nome do album fica o nome do artista quando baixa os metadados via shazam
#13 - organizar em pastas os componentes, criar pasta views
#14.1 - mudar classes para herdar as classes do flet diretamente, sem gambiarras, para melhorar a leitura (É melhor deixar como está, fica mais flexível o fluxo de updates da aplicação)
#14 - ao mudar de tab os elementos que são atualizados enquanto toca o audio não são encontrados pois eles são apagados da view, verificar possibilidade de apenas trocar eles de posição no array de controls da stack_main
#14.3 - colocar round_border na barra de tabs inferior
#14.4 - quando não houver músicas deve aparecer um ft.Text() avisando que não há músicas na playlist
#16 - adicionar campo de texto para indicar a quantidade de faixas num album na listagem para download




#14.2 - separar melhor os componentes a fim de diminuir códigos em um arquivo só
#15 - inluir nome do artista e album na pasta coverart para evitar conflitos de músicas com mesmo nome
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
#2- Resolver pequeno bug, quando uma música tá pausada e clica-se em outra, a que estava tocando começa a tocar em vez da que foi clicada, sendo necessário um segundo clique
#3- fazer uma geral nos arquivos, comentar o que for necessário, Incluir try catch onde necessita e informar o usuário quando houver um erro via notificação 
#4- resolver bug quando clica em adicionar música na playlist manualmente e não seleciona nenhuma, listen_view.py", line 67, in add_playlist_coverart
#5- adicionar tipagem em todos os parametros e retornos de todas as funções do ton player e do vlc_player e flet_player e da classe mãe player

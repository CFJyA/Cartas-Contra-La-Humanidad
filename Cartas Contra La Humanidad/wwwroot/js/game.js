// Cartas Contra La Humanidad - Main Multiplayer Client Logic
(function () {
    let connection = null;
    let currentRoom = null;
    let myPlayerId = localStorage.getItem('cah_playerId') || '';
    let myPlayerName = localStorage.getItem('cah_playerName') || '';
    let myAvatar = localStorage.getItem('cah_avatar') || '😎';
    let selectedCards = []; // Array of card objects currently selected to play
    let soundMuted = false;

    // Elements cache
    const screenWelcome = document.getElementById('screen-welcome');
    const screenLobby = document.getElementById('screen-lobby');
    const screenGame = document.getElementById('screen-game');

    // Init function
    function init() {
        initAvatars();
        initSignalR();
        checkUrlParams();
        setupEventListeners();
    }

    function initAvatars() {
        const avatars = ['😎', '😈', '🤡', '🍆', '💀', '🦄', '🌮', '💩', '👑', '👽', '🤖', '🐸', '🍕', '🍺', '💅', '🤠', '🦖', '🔥'];
        const container = document.getElementById('avatar-grid');
        if (!container) return;
        container.innerHTML = '';
        avatars.forEach(emoji => {
            const btn = document.createElement('div');
            btn.className = `avatar-option ${emoji === myAvatar ? 'active' : ''}`;
            btn.textContent = emoji;
            btn.onclick = () => {
                document.querySelectorAll('.avatar-option').forEach(el => el.classList.remove('active'));
                btn.classList.add('active');
                myAvatar = emoji;
                localStorage.setItem('cah_avatar', myAvatar);
                if (window.soundEngine) window.soundEngine.playCardClick();
            };
            container.appendChild(btn);
        });

        const nameInput = document.getElementById('input-player-name');
        if (nameInput && myPlayerName) {
            nameInput.value = myPlayerName;
        }
    }

    function checkUrlParams() {
        const urlParams = new URLSearchParams(window.location.search);
        const roomCode = urlParams.get('room');
        if (roomCode) {
            const joinInput = document.getElementById('input-join-code');
            if (joinInput) {
                joinInput.value = roomCode.toUpperCase();
                showTab('join');
            }
        }
    }

    function initSignalR() {
        connection = new signalR.HubConnectionBuilder()
            .withUrl("/gamehub")
            .withAutomaticReconnect([0, 2000, 5000, 10000])
            .build();

        connection.on("RoomUpdated", (state) => {
            currentRoom = state;
            renderRoom(state);
        });

        connection.on("ChatMessageReceived", (msg) => {
            appendChatMessage(msg);
        });

        connection.on("ReactionReceived", (data) => {
            showFloatingReaction(data.emoji, data.senderName);
            if (window.soundEngine) {
                if (data.emoji === '💩') window.soundEngine.playReaction('poop');
                else if (data.emoji === '👑') window.soundEngine.playReaction('crown');
                else window.soundEngine.playReaction('default');
            }
        });

        connection.on("TimerTick", (secondsLeft) => {
            updateTimerDisplay(secondsLeft);
            if (secondsLeft <= 5 && secondsLeft > 0 && window.soundEngine) {
                window.soundEngine.playTick();
            }
        });

        connection.start().then(() => {
            console.log("Conectado a SignalR Hub");
            // Auto-reconnect to room if present in session
            const savedRoom = sessionStorage.getItem('cah_active_room');
            if (savedRoom && myPlayerId) {
                joinRoom(savedRoom, true);
            }
        }).catch(err => {
            console.error("Error al conectar SignalR:", err);
            showToast("No se pudo conectar al servidor de juego.", "danger");
        });

        connection.onreconnected(() => {
            showToast("Conexión restablecida.", "success");
            const savedRoom = sessionStorage.getItem('cah_active_room');
            if (savedRoom && myPlayerId) {
                joinRoom(savedRoom, true);
            }
        });
    }

    function setupEventListeners() {
        // Toggle Audio
        const btnMute = document.getElementById('btn-toggle-sound');
        if (btnMute) {
            btnMute.onclick = () => {
                soundMuted = !soundMuted;
                if (window.soundEngine) window.soundEngine.enabled = !soundMuted;
                btnMute.innerHTML = soundMuted ? '🔇 Mudo' : '🔊 Sonido';
            };
        }

        // Chat Toggle
        const btnChat = document.getElementById('btn-toggle-chat');
        const chatDrawer = document.getElementById('chat-drawer');
        const btnCloseChat = document.getElementById('btn-close-chat');
        if (btnChat && chatDrawer) {
            btnChat.onclick = () => chatDrawer.classList.toggle('open');
        }
        if (btnCloseChat && chatDrawer) {
            btnCloseChat.onclick = () => chatDrawer.classList.remove('open');
        }

        // Chat Send
        const btnSendChat = document.getElementById('btn-send-chat');
        const inputChat = document.getElementById('input-chat-text');
        if (btnSendChat && inputChat) {
            const doSend = () => {
                const text = inputChat.value.trim();
                if (text && connection) {
                    connection.invoke("SendChat", text);
                    inputChat.value = '';
                }
            };
            btnSendChat.onclick = doSend;
            inputChat.onkeydown = (e) => { if (e.key === 'Enter') doSend(); };
        }

        // Reaction Bar Buttons
        document.querySelectorAll('.reaction-btn').forEach(btn => {
            btn.onclick = () => {
                const emoji = btn.dataset.emoji;
                if (emoji && connection) {
                    connection.invoke("SendReaction", emoji);
                    if (window.soundEngine) window.soundEngine.playCardClick();
                }
            };
        });

        // Copy room code / share link
        const btnCopyLink = document.getElementById('btn-copy-room-link');
        if (btnCopyLink) {
            btnCopyLink.onclick = copyRoomLink;
        }

        // QR Code modal trigger
        const btnShowQr = document.getElementById('btn-show-qr');
        if (btnShowQr) {
            btnShowQr.onclick = () => {
                generateQrCode();
            };
        }

        // Host controls
        const btnStartGame = document.getElementById('btn-start-game');
        if (btnStartGame) {
            btnStartGame.onclick = () => {
                if (connection) {
                    btnStartGame.disabled = true;
                    connection.invoke("StartGame").finally(() => {
                        btnStartGame.disabled = false;
                    });
                }
            };
        }

        const btnAddBot = document.getElementById('btn-add-bot');
        if (btnAddBot) {
            btnAddBot.onclick = () => {
                if (connection) connection.invoke("AddBot");
            };
        }

        // Next round
        const btnNextRound = document.getElementById('btn-next-round');
        if (btnNextRound) {
            btnNextRound.onclick = () => {
                if (connection) connection.invoke("NextRound");
            };
        }

        // Confirm Submit Play
        const btnConfirmPlay = document.getElementById('btn-confirm-play');
        if (btnConfirmPlay) {
            btnConfirmPlay.onclick = submitPlay;
        }

        // Leave room
        const btnLeave = document.getElementById('btn-leave-room');
        if (btnLeave) {
            btnLeave.onclick = leaveRoom;
        }

        // Custom Card Modal
        const btnSaveCustomCard = document.getElementById('btn-save-custom-card');
        if (btnSaveCustomCard) {
            btnSaveCustomCard.onclick = () => {
                const text = document.getElementById('custom-card-text').value.trim();
                const type = document.getElementById('custom-card-type').value;
                const pick = parseInt(document.getElementById('custom-card-pick').value) || 1;
                if (!text) return;

                if (connection) {
                    connection.invoke("AddCustomCard", text, type === 'black', pick);
                    const modal = bootstrap.Modal.getInstance(document.getElementById('modalCustomCard'));
                    if (modal) modal.hide();
                    document.getElementById('custom-card-text').value = '';
                    showToast("¡Carta personalizada agregada a la partida!", "success");
                }
            };
        }
    }

    // Public room actions
    window.createRoom = function () {
        const name = getPlayerName();
        if (!name) return;

        const targetScore = parseInt(document.getElementById('select-target-score').value) || 7;
        const timerSeconds = parseInt(document.getElementById('select-timer-seconds').value);
        const randoBot = document.getElementById('check-rando-bot').checked;

        if (!connection || connection.state !== signalR.HubConnectionState.Connected) {
            showToast("Conectando con el servidor, reintenta en un segundo...", "warning");
            return;
        }

        connection.invoke("CreateRoom", name, myAvatar, targetScore, timerSeconds, randoBot)
            .then(res => {
                if (res.success) {
                    myPlayerId = res.playerId;
                    localStorage.setItem('cah_playerId', myPlayerId);
                    sessionStorage.setItem('cah_active_room', res.roomCode);
                    if (window.soundEngine) window.soundEngine.playCardSubmit();
                }
            })
            .catch(err => {
                console.error("Error al crear sala:", err);
                showToast("No se pudo crear la sala.", "danger");
            });
    };

    window.joinRoom = function (codeOverride, silent = false) {
        const name = getPlayerName();
        if (!name) return;

        const codeInput = document.getElementById('input-join-code');
        const code = codeOverride || (codeInput ? codeInput.value.trim().toUpperCase() : '');

        if (!code) {
            showToast("Ingresa un código de sala válido.", "warning");
            return;
        }

        if (!connection || connection.state !== signalR.HubConnectionState.Connected) {
            if (!silent) showToast("Esperando conexión al servidor...", "warning");
            return;
        }

        connection.invoke("JoinRoom", code, myPlayerId, name, myAvatar)
            .then(res => {
                if (res.success) {
                    myPlayerId = res.playerId;
                    localStorage.setItem('cah_playerId', myPlayerId);
                    sessionStorage.setItem('cah_active_room', res.roomCode);
                    if (window.soundEngine) window.soundEngine.playCardClick();
                } else {
                    if (!silent) showToast(res.message, "danger");
                    sessionStorage.removeItem('cah_active_room');
                }
            })
            .catch(err => {
                console.error("Error al unirse a la sala:", err);
                if (!silent) showToast("Error al unirse a la sala.", "danger");
            });
    };

    function leaveRoom() {
        if (confirm("¿Seguro que deseas salir de la sala?")) {
            sessionStorage.removeItem('cah_active_room');
            if (connection) {
                connection.invoke("LeaveRoom").catch(() => {});
            }
            currentRoom = null;
            showScreen('welcome');
        }
    }

    function getPlayerName() {
        const input = document.getElementById('input-player-name');
        const val = input ? input.value.trim() : '';
        if (!val) {
            showToast("Por favor ingresa un apodo para jugar.", "warning");
            if (input) input.focus();
            return null;
        }
        myPlayerName = val;
        localStorage.setItem('cah_playerName', myPlayerName);
        return val;
    }

    function copyRoomLink() {
        if (!currentRoom) return;
        const url = `${window.location.origin}${window.location.pathname}?room=${currentRoom.code}`;
        navigator.clipboard.writeText(url).then(() => {
            showToast("¡Enlace de sala copiado al portapapeles! Envíalo a tus compas.", "success");
            if (window.soundEngine) window.soundEngine.playCardClick();
        }).catch(() => {
            prompt("Copia este enlace para invitar a tus amigos:", url);
        });
    }

    function generateQrCode() {
        const container = document.getElementById('qrcode-container');
        const urlLabel = document.getElementById('qr-target-url');
        if (!container || !currentRoom) return;

        const mobileHost = window.cah_hotspotHost || window.location.host;
        const joinUrl = `http://${mobileHost}/?room=${currentRoom.code}`;

        container.innerHTML = '';
        if (window.QRCode) {
            new QRCode(container, {
                text: joinUrl,
                width: 180,
                height: 180,
                colorDark: "#000000",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.M
            });
        }
        if (urlLabel) urlLabel.textContent = joinUrl;
    }

    // Main Renderer
    function renderRoom(room) {
        if (!room) {
            showScreen('welcome');
            return;
        }

        // Update header room code badge
        const badgeRoomCode = document.getElementById('header-room-code');
        if (badgeRoomCode) badgeRoomCode.textContent = room.code;

        // Route screens
        if (room.state === 'Lobby') {
            showScreen('lobby');
            renderLobby(room);
        } else {
            showScreen('game');
            renderGame(room);
        }
    }

    function showScreen(name) {
        screenWelcome.classList.add('d-none');
        screenLobby.classList.add('d-none');
        screenGame.classList.add('d-none');

        if (name === 'welcome') screenWelcome.classList.remove('d-none');
        else if (name === 'lobby') screenLobby.classList.remove('d-none');
        else if (name === 'game') screenGame.classList.remove('d-none');
    }

    // Lobby Renderer
    function renderLobby(room) {
        document.getElementById('lobby-room-code').textContent = room.code;

        // Render player list
        const grid = document.getElementById('lobby-players-grid');
        grid.innerHTML = '';

        room.players.forEach(p => {
            const card = document.createElement('div');
            card.className = 'player-lobby-card';
            card.innerHTML = `
                <div class="player-avatar-circle">${p.avatar}</div>
                <div style="flex:1; min-width:0;">
                    <div class="player-name-text">${escapeHtml(p.name)}</div>
                    <div style="display:flex; gap:4px; margin-top:2px;">
                        ${p.isHost ? '<span class="badge-host">👑 Anfitrión</span>' : ''}
                        ${p.isBot ? '<span class="badge-czar">🤖 Bot</span>' : ''}
                        ${p.id === myPlayerId ? '<span class="badge bg-secondary" style="font-size:0.65rem;">Tú</span>' : ''}
                    </div>
                </div>
                ${(room.amIHost && p.isBot) ? `<button class="btn btn-sm btn-outline-danger" title="Eliminar Bot" onclick="removeBot('${p.id}')">✕</button>` : ''}
            `;
            grid.appendChild(card);
        });

        // Host controls
        const hostControls = document.getElementById('lobby-host-controls');
        const waitingNotice = document.getElementById('lobby-waiting-notice');
        const startBtn = document.getElementById('btn-start-game');

        if (room.amIHost) {
            hostControls.classList.remove('d-none');
            waitingNotice.classList.add('d-none');

            // Must have at least 2 players (or 1 human + bots)
            if (room.players.length < 2) {
                startBtn.disabled = true;
                startBtn.title = "Se necesitan al menos 2 jugadores (puedes agregar un bot)";
            } else {
                startBtn.disabled = false;
                startBtn.title = "";
            }
        } else {
            hostControls.classList.add('d-none');
            waitingNotice.classList.remove('d-none');
        }
    }

    window.removeBot = function (botId) {
        if (connection) connection.invoke("RemoveBot", botId);
    };

    // Game Renderer
    function renderGame(room) {
        renderTopBar(room);
        renderBlackCard(room.activeBlackCard);

        const stageJudging = document.getElementById('stage-judging');
        const stagePlaying = document.getElementById('stage-playing');
        const stageWinner = document.getElementById('stage-winner');
        const stageGameOver = document.getElementById('stage-gameover');
        const handSection = document.getElementById('hand-section');

        stageJudging.classList.add('d-none');
        stagePlaying.classList.add('d-none');
        stageWinner.classList.add('d-none');
        stageGameOver.classList.add('d-none');
        handSection.classList.add('d-none');

        if (room.state === 'Playing') {
            stagePlaying.classList.remove('d-none');
            renderPlayingState(room);
        } else if (room.state === 'Judging') {
            stageJudging.classList.remove('d-none');
            renderJudgingState(room);
        } else if (room.state === 'RoundResults') {
            stageWinner.classList.remove('d-none');
            renderWinnerState(room);
        } else if (room.state === 'GameOver') {
            stageGameOver.classList.remove('d-none');
            renderGameOverState(room);
        }
    }

    function renderTopBar(room) {
        document.getElementById('top-round-number').textContent = room.currentRound;
        document.getElementById('top-target-score').textContent = room.targetScore;
        document.getElementById('top-czar-avatar').textContent = room.czarAvatar;
        document.getElementById('top-czar-name').textContent = room.czarName;

        // Scoreboard chips
        const scoreContainer = document.getElementById('top-scoreboard');
        scoreContainer.innerHTML = '';

        room.players.forEach(p => {
            const chip = document.createElement('div');
            chip.className = `player-score-chip ${p.isCzar ? 'is-czar' : ''} ${p.id === myPlayerId ? 'is-me' : ''}`;
            chip.innerHTML = `
                <span>${p.avatar}</span>
                <span>${escapeHtml(p.name)}</span>
                <span class="badge bg-warning text-dark" style="font-weight:900;">${p.score}</span>
                ${p.hasSubmitted && room.state === 'Playing' && !p.isCzar ? '<span title="Listo">✅</span>' : ''}
            `;
            scoreContainer.appendChild(chip);
        });

        updateTimerDisplay(room.timeRemaining);
    }

    function updateTimerDisplay(seconds) {
        const timerEl = document.getElementById('top-timer');
        if (!timerEl) return;
        if (currentRoom && currentRoom.roundTimerSeconds === 0) {
            timerEl.innerHTML = `⏱️ ∞`;
            return;
        }

        timerEl.innerHTML = `⏱️ ${seconds}s`;
        if (seconds <= 10 && seconds > 0) {
            timerEl.classList.add('timer-danger');
        } else {
            timerEl.classList.remove('timer-danger');
        }
    }

    function renderBlackCard(card) {
        const container = document.getElementById('active-black-card');
        if (!container || !card) return;

        // Replace blank underscores with styled span
        let formattedText = escapeHtml(card.text).replace(/______/g, '<span class="blank-highlight">______</span>');

        container.innerHTML = `
            <div class="cah-card card-black">
                <div class="card-text">${formattedText}</div>
                <div class="card-footer-cah">
                    <div class="card-watermark">
                        <span>🃏</span> Cartas Contra La Humanidad
                    </div>
                    <div>
                        ${card.pick > 1 ? `<span class="card-badge">ELIGE ${card.pick}</span>` : ''}
                        ${card.draw > 0 ? `<span class="card-badge bg-danger text-white">ROBA ${card.draw}</span>` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    function renderPlayingState(room) {
        const czarBanner = document.getElementById('playing-czar-banner');
        const playerArea = document.getElementById('playing-player-area');
        const handSection = document.getElementById('hand-section');

        if (room.amICzar) {
            czarBanner.classList.remove('d-none');
            playerArea.classList.add('d-none');
            handSection.classList.add('d-none');

            // Render submission progress for Czar
            const progressList = document.getElementById('czar-submission-progress');
            progressList.innerHTML = '';
            room.players.filter(p => !p.isCzar).forEach(p => {
                const item = document.createElement('div');
                item.className = 'player-score-chip';
                item.innerHTML = `
                    <span>${p.avatar}</span>
                    <span>${escapeHtml(p.name)}</span>
                    <span>${p.hasSubmitted ? '✅ Jugó' : '⏳ Pensando...'}</span>
                `;
                progressList.appendChild(item);
            });
        } else {
            czarBanner.classList.add('d-none');
            playerArea.classList.remove('d-none');
            handSection.classList.remove('d-none');

            const hasSubmitted = room.mySubmittedCards && room.mySubmittedCards.length > 0;
            const btnConfirm = document.getElementById('btn-confirm-play');

            if (hasSubmitted) {
                // Show already submitted cards in slots
                renderSlots(room.activeBlackCard.pick, room.mySubmittedCards, true);
                btnConfirm.classList.add('d-none');
                document.getElementById('playing-instruction').innerHTML = `
                    <div class="alert alert-success d-inline-block p-2 mb-0">
                        ✨ ¡Ya jugaste tus cartas! Esperando a los demás jugadores...
                    </div>
                `;
                renderHand(room.myHand, false);
            } else {
                renderSlots(room.activeBlackCard.pick, selectedCards, false);
                btnConfirm.classList.remove('d-none');
                btnConfirm.disabled = selectedCards.length !== room.activeBlackCard.pick;
                document.getElementById('playing-instruction').textContent = 
                    `Elige ${room.activeBlackCard.pick} carta${room.activeBlackCard.pick > 1 ? 's' : ''} de tu mano (${selectedCards.length}/${room.activeBlackCard.pick})`;
                renderHand(room.myHand, true);
            }
        }
    }

    function renderSlots(pickCount, cards, isLocked) {
        const slotsGrid = document.getElementById('playing-slots-grid');
        slotsGrid.innerHTML = '';

        for (let i = 0; i < pickCount; i++) {
            const slot = document.createElement('div');
            const card = cards[i];

            if (card) {
                slot.className = 'card-slot has-card';
                slot.innerHTML = `
                    <div class="cah-card card-white" style="width:100%; height:100%; min-height:200px;">
                        <div class="selection-order-badge">${i + 1}</div>
                        <div class="card-text">${escapeHtml(card.text)}</div>
                        <div class="card-footer-cah">
                            <div class="card-watermark"><span>🃏</span> CAH</div>
                            ${!isLocked ? `<span style="color:#ef4444; cursor:pointer;" onclick="deselectSlot(${i})">✕ Quitar</span>` : ''}
                        </div>
                    </div>
                `;
            } else {
                slot.className = 'card-slot';
                slot.innerHTML = `
                    <div style="font-size:2rem; opacity:0.3;">🃏</div>
                    <div>Carta #${i + 1}</div>
                    <div style="font-size:0.75rem; opacity:0.6;">Selecciona de tu mano</div>
                `;
            }

            slotsGrid.appendChild(slot);
        }
    }

    window.deselectSlot = function (index) {
        if (selectedCards[index]) {
            selectedCards.splice(index, 1);
            if (window.soundEngine) window.soundEngine.playCardClick();
            if (currentRoom) renderPlayingState(currentRoom);
        }
    };

    function renderHand(hand, isInteractive) {
        const container = document.getElementById('hand-cards-grid');
        container.innerHTML = '';

        hand.forEach(card => {
            const cardEl = document.createElement('div');
            const selectedIdx = selectedCards.findIndex(c => c.id === card.id);
            const isSelected = selectedIdx !== -1;

            cardEl.className = `cah-card card-white ${isSelected ? 'selected' : ''}`;
            cardEl.innerHTML = `
                ${isSelected ? `<div class="selection-order-badge">${selectedIdx + 1}</div>` : ''}
                <div class="card-text">${escapeHtml(card.text)}</div>
                <div class="card-footer-cah">
                    <div class="card-watermark"><span>🃏</span> Cartas Contra La Humanidad</div>
                </div>
            `;

            if (isInteractive) {
                cardEl.onclick = () => {
                    const pickNeeded = currentRoom.activeBlackCard.pick;

                    if (isSelected) {
                        // Deselect
                        selectedCards.splice(selectedIdx, 1);
                    } else {
                        // Select
                        if (selectedCards.length < pickNeeded) {
                            selectedCards.push(card);
                        } else if (pickNeeded === 1) {
                            selectedCards = [card]; // Swap if only 1 card needed
                        } else {
                            showToast(`Ya seleccionaste las ${pickNeeded} cartas necesarias.`, "warning");
                            return;
                        }
                    }

                    if (window.soundEngine) window.soundEngine.playCardClick();
                    renderPlayingState(currentRoom);
                };
            } else {
                cardEl.style.cursor = 'default';
            }

            container.appendChild(cardEl);
        });
    }

    function submitPlay() {
        if (!currentRoom || !connection) return;
        const required = currentRoom.activeBlackCard.pick;
        if (selectedCards.length !== required) {
            showToast(`Debes elegir exactamente ${required} cartas.`, "warning");
            return;
        }

        const cardIds = selectedCards.map(c => c.id);
        connection.invoke("SubmitCards", cardIds)
            .then(() => {
                if (window.soundEngine) window.soundEngine.playCardSubmit();
                selectedCards = [];
            })
            .catch(err => {
                console.error("Error al enviar jugada:", err);
                showToast("Error al enviar la jugada.", "danger");
            });
    }

    // Judging Renderer
    function renderJudgingState(room) {
        const titleEl = document.getElementById('judging-status-title');
        const container = document.getElementById('judging-submissions-grid');
        container.innerHTML = '';

        if (room.amICzar) {
            titleEl.innerHTML = `👑 <strong>¡Eres el Zar!</strong> Elige la respuesta más graciosa o culera:`;
        } else {
            titleEl.innerHTML = `⚖️ El Zar <strong>${escapeHtml(room.czarName)}</strong> está juzgando las respuestas...`;
        }

        room.submissions.forEach((sub, idx) => {
            const group = document.createElement('div');
            group.className = 'submission-group';

            let cardsHtml = '';
            sub.cards.forEach((c, cIdx) => {
                cardsHtml += `
                    <div class="cah-card card-white" style="min-height:160px;">
                        ${sub.cards.length > 1 ? `<div class="selection-order-badge" style="width:22px; height:22px; font-size:0.75rem;">${cIdx + 1}</div>` : ''}
                        <div class="card-text" style="font-size:0.95rem;">${escapeHtml(c.text)}</div>
                    </div>
                `;
            });

            group.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="badge bg-secondary">Opción #${idx + 1}</span>
                    ${room.amICzar ? `<button class="btn btn-sm btn-cah-accent">👑 Elegir Ganador</button>` : ''}
                </div>
                ${cardsHtml}
            `;

            if (room.amICzar) {
                group.onclick = () => {
                    chooseWinner(sub.id);
                };
            }

            container.appendChild(group);
        });
    }

    function chooseWinner(submissionId) {
        if (!connection) return;
        if (window.soundEngine) window.soundEngine.playCardSubmit();
        connection.invoke("SelectWinner", submissionId).catch(err => {
            console.error("Error al elegir ganador:", err);
        });
    }

    // Winner Reveal Renderer
    function renderWinnerState(room) {
        if (window.confetti) {
            confetti({
                particleCount: 120,
                spread: 80,
                origin: { y: 0.6 }
            });
        }
        if (window.soundEngine) window.soundEngine.playWinnerFanfare();

        const banner = document.getElementById('winner-reveal-banner');
        const winnerCardContainer = document.getElementById('winner-card-combo');

        const winnerName = room.winnerPlayerName || 'Alguien';
        banner.innerHTML = `
            <div style="font-size:3rem; margin-bottom:0.5rem;">🎉🏆👑</div>
            <h2 style="font-weight:900; color:var(--accent-gold); margin:0;">
                ¡${escapeHtml(winnerName)} GANA LA RONDA!
            </h2>
            <p style="color:var(--text-secondary); margin-top:0.5rem;">Se lleva un Asombroso Punto ⭐️</p>
        `;

        winnerCardContainer.innerHTML = '';
        if (room.winningSubmission) {
            room.winningSubmission.cards.forEach((c, idx) => {
                const cardEl = document.createElement('div');
                cardEl.className = 'cah-card card-white is-winner-card';
                cardEl.style.minWidth = '220px';
                cardEl.innerHTML = `
                    ${room.winningSubmission.cards.length > 1 ? `<div class="selection-order-badge">${idx + 1}</div>` : ''}
                    <div class="card-text">${escapeHtml(c.text)}</div>
                    <div class="card-footer-cah">
                        <div class="card-watermark"><span>🏆</span> Jugada por ${escapeHtml(room.winningSubmission.playerName)}</div>
                    </div>
                `;
                winnerCardContainer.appendChild(cardEl);
            });
        }

        // Host / Czar can advance immediately or auto countdown
        const nextBtn = document.getElementById('btn-next-round');
        if (room.amIHost || room.amICzar) {
            nextBtn.classList.remove('d-none');
            nextBtn.textContent = "➡️ Siguiente Ronda";
        } else {
            nextBtn.classList.add('d-none');
        }
    }

    // Game Over Podium Renderer
    function renderGameOverState(room) {
        if (window.confetti) {
            confetti({
                particleCount: 250,
                spread: 120,
                origin: { y: 0.5 }
            });
        }
        if (window.soundEngine) window.soundEngine.playWinnerFanfare();

        const sorted = [...room.players].sort((a, b) => b.score - a.score);
        const podiumContainer = document.getElementById('gameover-podium');
        podiumContainer.innerHTML = '';

        const medals = ['🥇', '🥈', '🥉'];
        sorted.slice(0, 3).forEach((p, idx) => {
            const pod = document.createElement('div');
            pod.className = 'player-lobby-card';
            pod.style.borderColor = idx === 0 ? 'var(--accent-gold)' : 'var(--border-color)';
            pod.innerHTML = `
                <div style="font-size:2.5rem;">${medals[idx]}</div>
                <div class="player-avatar-circle" style="font-size:2rem;">${p.avatar}</div>
                <div>
                    <h4 style="margin:0; font-weight:900;">${escapeHtml(p.name)}</h4>
                    <div style="color:var(--accent-gold); font-weight:800;">${p.score} Puntos Asombrosos</div>
                </div>
            `;
            podiumContainer.appendChild(pod);
        });

        const btnRestart = document.getElementById('btn-restart-game');
        if (room.amIHost) {
            btnRestart.classList.remove('d-none');
            btnRestart.onclick = () => {
                if (connection) connection.invoke("NextRound");
            };
        } else {
            btnRestart.classList.add('d-none');
        }
    }

    // Chat logic
    function appendChatMessage(msg) {
        const container = document.getElementById('chat-messages-box');
        if (!container) return;

        const bubble = document.createElement('div');
        bubble.className = `chat-message-bubble ${msg.isSystem ? 'chat-system' : ''}`;
        bubble.innerHTML = `
            ${!msg.isSystem ? `<div class="chat-sender">${escapeHtml(msg.senderAvatar)} ${escapeHtml(msg.senderName)}</div>` : ''}
            <div>${escapeHtml(msg.text)}</div>
        `;
        container.appendChild(bubble);
        container.scrollTop = container.scrollHeight;
    }

    // Floating reaction animation
    function showFloatingReaction(emoji, sender) {
        const container = document.getElementById('floating-reaction-container');
        if (!container) return;

        const el = document.createElement('div');
        el.className = 'floating-reaction';
        el.textContent = emoji;

        // Random X position between 10% and 85%
        const randomX = Math.floor(Math.random() * 75) + 10;
        el.style.left = `${randomX}%`;

        container.appendChild(el);
        setTimeout(() => {
            el.remove();
        }, 2900);
    }

    // Helper functions
    function showToast(message, type = 'info') {
        const toastEl = document.getElementById('liveToast');
        const bodyEl = document.getElementById('toast-body');
        if (!toastEl || !bodyEl) return;

        bodyEl.textContent = message;
        toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
        const toast = new bootstrap.Toast(toastEl, { delay: 3500 });
        toast.show();
    }

    window.showTab = function (tab) {
        document.querySelectorAll('.welcome-tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.welcome-tab-content').forEach(c => c.classList.add('d-none'));

        const targetBtn = document.getElementById(`tab-btn-${tab}`);
        const targetContent = document.getElementById(`tab-content-${tab}`);
        if (targetBtn) targetBtn.classList.add('active');
        if (targetContent) targetContent.classList.remove('d-none');
    };

    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    // Launch!
    window.addEventListener('DOMContentLoaded', init);
})();

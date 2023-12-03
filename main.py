import webview
from decimal import Decimal

class Vertex:
    def __init__(self, label: str  = None, weight: int = float("inf"), index: int = None):
        self.label: str = label
        self.weight: int = weight
        self.index: int = index


class Graph:
    def __init__(self, size: int = 10):
        self.size: int = size
        self.index: int = 0
        self.vertices_list: list = [None] * self.size
        self.vertices: dict = {}
        self.adjacency_matrix: list = [[None for i in range(self.size)] for j in range(self.size)]
        self.prev: dict = {}
        self.visited: dict = {}

    def add_vertex(self, label: str):
        if self.index == self.size:  # matrix is full
            return
        vertex: Vertex = Vertex(label, float("inf"), self.index)
        self.vertices_list[self.index] = vertex
        self.vertices[vertex.label] = vertex
        self.index += 1
        self.prev[vertex.label] = None
        self.visited[vertex.label] = False

    def add_edge(self, label1: str, label2: str, weight: int):
        index1: int = self.vertices[label1].index
        index2: int = self.vertices[label2].index
        self.adjacency_matrix[index1][index2] = weight

    def dijkstra(self, label: str):
        current_vertex: Vertex = self.vertices[label]
        current_vertex.weight = 0
        while current_vertex is not None:
            self.visited[current_vertex.label] = True
            for i in range(self.index):
                if self.adjacency_matrix[current_vertex.index][i] is not None:
                    weight: int = self.adjacency_matrix[current_vertex.index][i]
                    neighbour: Vertex = self.vertices_list[i]
                    if current_vertex.weight + weight < neighbour.weight:
                        neighbour.weight = current_vertex.weight + weight
                        self.prev[neighbour.label] = current_vertex.label
            current_vertex = self.find_minimum_weight_vertex()

    def return_path(self, label: str) -> str:
        if self.prev[label] is None:
            return label
        else:
            return self.return_path(self.prev[label]) + " -> " + label

    def find_minimum_weight_vertex(self):
        vertex: Vertex = None
        for label in self.vertices:
            if not self.visited[label]:
                if vertex is None:
                    vertex = self.vertices[label]
                else:
                    if vertex.weight > self.vertices[label].weight:
                        vertex = self.vertices[label]
        return vertex
        
    def hitung_panjang_edge_tercepat(self, label_awal: str, label_akhir: str) -> int:
        jalur_tercepat = self.return_path(label_akhir)
        if jalur_tercepat == label_akhir:
            return 0  # Jika hanya satu vertex, maka panjang edge adalah 0

        jalur_list = jalur_tercepat.split(" -> ")
        total_bobot = 0
        for i in range(len(jalur_list) - 1):
            idx_awal = int(jalur_list[i])
            idx_akhir = int(jalur_list[i + 1])
            total_bobot += self.adjacency_matrix[idx_awal][idx_akhir]

        return total_bobot


def main():
    # Embedded HTML content
    html_content = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Dijkstra</title>
    <style>
        body {
            font-family: Arial, sans-serif;

            background-color: #f0f0f0;
        }

        #container {
            text-align: center;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        canvas {
            border: 1px solid black;
            cursor: pointer;
            margin-top: 10px;
        }

        form {
            margin-bottom: 10px;
        }

        button {
            padding: 8px 16px;
            margin-right: 10px;
            cursor: pointer;
            background-color: #007bff;
            color: #fff;
            border: none;
            border-radius: 4px;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #0056b3;
        }

        input {
            padding: 6px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }

        .button-group {
            display: flex;
            justify-content: center;
            margin-top: 15px;
        }

        .button-group button {
            margin: 0 5px;
        }

        /* Gaya untuk modal */
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0, 0, 0, 0.4);
        }

        .modal-content {
            background-color: #fefefe;
            margin: 10% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 30%;
            border-radius: 6px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .modal-content-small {
            background-color: #fefefe;
            margin: 10% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 20%;
            border-radius: 6px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .modal-content-large {
            background-color: #fefefe;
            margin: 10% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 50%;
            border-radius: 6px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }

        .close:hover,
        .close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }
    </style>
</head>

<body>

    <div id="container">
        <!-- <h1>Dijkstra</h1> -->
        <form id="vertexForm">
            <button type="button" onclick="showAboutUsModal()">Tentang Kami</button>

            <label for="vertexCount">Jumlah Vertex:</label>
            <input type="number" id="vertexCount" name="vertexCount" min="2" value="3">
            <button type="button" onclick="changeVertexCount()">Inisialisasi</button>
            <!-- <button onclick="resetCanvas()">Reset Canvas</button> -->

        </form>
        <canvas id="canvas" width="600" height="400"></canvas>
        <div class="button-group">
            <button onclick="setMode('move')">Pindah Vertex</button>
            <button onclick="addVertex()">Tambah Vertex</button>
            <button onclick="removeVertex()">Hapus Vertex Akhir</button>
            <button onclick="setMode('edge')">Tambah Edge</button>

        </div>
        <p></p>
        <div id="dijkstraInput">
            <label for="startVertex">Vertex Awal:</label>
            <input type="number" id="startVertex" name="startVertex" value="0">
            <label for="endVertex">Vertex Akhir:</label>
            <input type="number" id="endVertex" name="endVertex" value="2">
            <button onclick="runDijkstra()">Jalankan Dijkstra</button>

        </div>
    </div>

    <!-- Tambahkan modal -->
<div id="myModal" class="modal">
    <div class="modal-content">
      <span class="close">&times;</span>
      <p id="modalText"></p>
      <input type="text" id="modalInput" style="display: none;">
      <button id="modalButton" style="display: none;margin-top: 10px;">OK</button>
    </div>
  </div>

  <div id="myModal2" class="modal">
    <div class="modal-content-small">
        <div class="button-group">
            <button id="ubahButton" class="modal-button">Ubah</button>
            <button id="hapusButton" class="modal-button" style="background-color: red;">Hapus</button>
        </div>
    </div>
  </div>
  


<div id="myModalAbout" class="modal">
    <div class="modal-content-large">
      <div style="text-align: center;">
        <p>Dijkstra Visualization dibuat oleh</p>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>NRP</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Aditya Nanda Utama</td>
                    <td>6026231036</td>
                </tr>
                <tr>
                    <td>Airlangga Bayu Satriawan</td>
                    <td>6026231006</td>
                </tr>
                <tr>
                    <td>Alvin Tarisa Akbar</td>
                    <td>6026231009</td>
                </tr>
            </tbody>
        </table>
        <p>Infrastruktur Teknologi Informasi <br><br> Institut Teknologi Sepuluh Nopember</p>
      </div>
      <button id="modalButtonAbout" style="margin-top: 10px;">OK</button>

    </div>
  </div>

  <script>
    const modalButtonAbout = document.getElementById('modalButtonAbout');
    const aboutUsModal = document.getElementById('myModalAbout');

    window.addEventListener('pywebviewready', function() {
        showAboutUsModal();

    })

    modalButtonAbout.onclick = function() {
        aboutUsModal.style.display = 'none';
      }
    function showAboutUsModal() {

        pywebview.api.sendAbout();
        // aboutUsModal.style.display = 'block';

    }

    let inputValue = null; // Variabel untuk menyimpan nilai yang diinput
  
    // Fungsi untuk menampilkan modal dengan pesan tertentu
    function showModal(message, input = false) {
      const modal = document.getElementById('myModal');
      const modalText = document.getElementById('modalText');
      const modalInput = document.getElementById('modalInput');
      const modalButton = document.getElementById('modalButton');
  
      modalText.textContent = message;
      if (input) {
        modalInput.style.display = 'block';
        modalButton.style.display = 'block';
      } else {
        //modalInput.style.display = 'none';
        //modalButton.style.display = 'none';

        return pywebview.api.sendErrorWarning(message);
      }
  
      modal.style.display = 'block';
  
      // Aksi saat tombol OK pada modal ditekan
      modalButton.onclick = function() {
        const newValue = modalInput.value;
        if (newValue.trim() !== '') {
          inputValue = newValue; // Menyimpan nilai yang diinput
          modal.style.display = 'none';
        } else {
          showModal('Silakan masukkan nilai yang valid.');
        }
      }
  
      // Aksi saat tombol close pada modal ditekan
      const spanClose = document.getElementsByClassName('close')[0];
      spanClose.onclick = function() {
        modal.style.display = 'none';
      }
  
      // Aksi saat pengguna mengklik area di luar modal (untuk menutup modal)
      window.onclick = function(event) {
        if (event.target === modal) {
          modal.style.display = 'none';
        }
      }
    }

    function showModal2(message, input = false) {
        const modal = document.getElementById('myModal2');

    
        modal.style.display = 'block';
    
    
        // Aksi saat tombol close pada modal ditekan
        const spanClose = document.getElementsByClassName('close')[0];
        spanClose.onclick = function() {
          modal.style.display = 'none';
        }
    
        // Aksi saat pengguna mengklik area di luar modal (untuk menutup modal)
        window.onclick = function(event) {
          if (event.target === modal) {
            modal.style.display = 'none';
          }
        }
      }
  
    // Fungsi untuk menampilkan dialog input dan mengembalikan nilai yang diinput
    function showInputDialog1(message, clickedEdgeIndex) {
        document.getElementById('modalInput').value = null;
    
        showModal2(message, false);
    
       
        const spanClose = document.querySelector('.close');
        spanClose.onclick = function () {
            modalContent.innerHTML = ''; // Menghapus konten modal saat ditutup
            const modal = document.getElementById('myModal2');
            modal.style.display = 'none';
        }
    
        const ubahButton = document.getElementById('ubahButton');
        const hapusButton = document.getElementById('hapusButton');
    
        ubahButton.onclick = function () {
            const modal = document.getElementById('myModal2');
            modal.style.display = 'none';

            
            showInputDialog2('Masukkan nilai baru untuk edge:', clickedEdgeIndex);
        }
    
        hapusButton.onclick = function () {

            const modal = document.getElementById('myModal2');
            modal.style.display = 'none';
            
            vertices[clickedEdgeIndex.from].edges.splice(clickedEdgeIndex.to, 1);
            vertices[clickedEdgeIndex.from].edgeValues.splice(clickedEdgeIndex.to, 1);
            draw();
        }
    
        
    }
    

    // Fungsi untuk menampilkan dialog input dan mengembalikan nilai yang diinput
    function showInputDialog2(message,clickedEdgeIndex) {
        document.getElementById('modalInput').value = null;
        showModal(message, true);
        const modalButton = document.getElementById('modalButton');
        modalButton.textContent = 'OK';
        modalButton.style.display = 'block';
        // Mengembalikan nilai yang diinput ketika modal ditutup
        return new Promise((resolve, reject) => {
          modalButton.onclick = function() {
            if (document.getElementById('modalInput').value !== null) {
                const newValue = document.getElementById('modalInput').value;
                if (newValue !== null && newValue.trim() !== '') {
                    vertices[clickedEdgeIndex.from].edgeValues[clickedEdgeIndex.to] = parseInt(newValue);
                    draw();
                    document.getElementById('myModal').style.display = 'none';
                }
            } else {
              reject('Tidak ada nilai yang diinput.');
            }
          }
        });
      }

      // Fungsi untuk menampilkan dialog input dan mengembalikan nilai yang diinput
    function showInputDialog3(message,edgeStart,endVertex) {
        document.getElementById('modalInput').value = null;
        showModal(message, true);
        const modalButton = document.getElementById('modalButton');
        modalButton.textContent = 'OK';
        modalButton.style.display = 'block';
        // Mengembalikan nilai yang diinput ketika modal ditutup
        return new Promise((resolve, reject) => {
          modalButton.onclick = function() {
            if (document.getElementById('modalInput').value !== null) {
                const value = document.getElementById('modalInput').value;
                if (value !== null && value.trim() !== '') {
                    vertices[edgeStart].edges.push(endVertex);
                    vertices[edgeStart].edgeValues.push(parseInt(value));
                    draw();
                    document.getElementById('myModal').style.display = 'none';
                }
            } else {
              reject('Tidak ada nilai yang diinput.');
            }
          }
        });
      }
  
    // Di dalam kode Anda, gunakan fungsi showInputDialog untuk menampilkan modal dialog input
    // dan gunakan nilai yang dikembalikan (dengan menggunakan Promise) untuk melakukan sesuatu
    // dengan nilai yang diinput, seperti mengubah nilai edge atau melakukan tindakan lainnya.
  </script>
  
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let vertexCount = 3;
        let vertices = [];
        let mode = 'move';
        let dragging = false;
        let selectedVertex = null;
        let edgeStart = null;
        let deleteEdgeTimeout = null;

        function resetCanvas() {
            vertices = []; // Menghapus semua vertices
            draw(); // Menggambar kembali canvas yang kosong
        }



        function clearCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }

        function drawVertex(x, y, label) {
            ctx.beginPath();
            ctx.arc(x, y, 12, 0, Math.PI * 2); // Ubah ukuran vertex menjadi 12
            ctx.fillStyle = 'blue';
            ctx.fill();
            ctx.closePath();
            ctx.font = 'bold 14px Arial'; // Tambahkan "bold" untuk label vertex
            ctx.fillStyle = 'white';
            ctx.fillText(label, x - 6, y + 5); // Beri padding untuk label
        }

        function drawEdge(startX, startY, endX, endY, value) {
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(endX, endY);
            ctx.strokeStyle = 'black';
            ctx.stroke();
            if (value !== undefined) {
                ctx.font = '14px Arial';
                ctx.fillStyle = 'black';
                ctx.fillText(value, (startX + endX) / 2, (startY + endY) / 2);
            }
            ctx.closePath();
        }

        function draw() {
            clearCanvas();
            for (let i = 0; i < vertices.length; i++) {
                for (let j = 0; j < vertices[i].edges.length; j++) {
                    const endVertex = vertices[vertices[i].edges[j]];
                    drawEdge(
                        vertices[i].x,
                        vertices[i].y,
                        endVertex.x,
                        endVertex.y,
                        vertices[i].edgeValues[j]
                    );
                }
            }
            for (let i = 0; i < vertices.length; i++) {
                const label = drawNextVertexLabel(i);
                drawVertex(vertices[i].x, vertices[i].y, label);
            }
            if (edgeStart !== null && mode === 'edge') {
                const {
                    x,
                    y
                } = getCursorPosition(event);
                drawEdge(vertices[edgeStart].x, vertices[edgeStart].y, x, y);
            }
        }


        function getRandomPosition() {
            const x = Math.floor(Math.random() * (canvas.width - 20)) + 10;
            const y = Math.floor(Math.random() * (canvas.height - 20)) + 10;
            return {
                x,
                y
            };
        }

        function addVertex() {
            const {
                x,
                y
            } = getRandomPosition();
            vertices.push({
                x,
                y,
                edges: [],
                edgeValues: []
            });
            draw();
        }

        function getCursorPosition(event) {
            const rect = canvas.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            return {
                x,
                y
            };
        }

        function checkClickedVertex(cursorX, cursorY) {
            for (let i = 0; i < vertices.length; i++) {
                const distance = Math.sqrt((cursorX - vertices[i].x) ** 2 + (cursorY - vertices[i].y) ** 2);
                if (distance <= 8) {
                    return i;
                }
            }
            return null;
        }

        canvas.addEventListener('mousedown', function(event) {
            const {
                x,
                y
            } = getCursorPosition(event);
            selectedVertex = checkClickedVertex(x, y);
            if (selectedVertex !== null && mode === 'move') {
                dragging = true;
            } else if (mode === 'edge') {
                edgeStart = checkClickedVertex(x, y);
            } else {
                // Jika mode bukan 'move' atau 'edge', maka cek apakah klik dilakukan di atas edge
                const clickedEdgeIndex = checkClickedEdge(x, y);
                if (clickedEdgeIndex !== null) {
                    showInputDialog1('Pilih:',clickedEdgeIndex);
                    
                }
            }
        });

        canvas.addEventListener('mousemove', function(event) {
            if (dragging && selectedVertex !== null && mode === 'move') {
                const {
                    x,
                    y
                } = getCursorPosition(event);
                vertices[selectedVertex].x = x;
                vertices[selectedVertex].y = y;
                draw();
            } else if (edgeStart !== null && mode === 'edge') {
                draw();
            }
        });

        canvas.addEventListener('mouseup', function(event) {
            if (dragging && selectedVertex !== null && mode === 'move') {
                dragging = false;
                selectedVertex = null;
            } else if (edgeStart !== null && mode === 'edge') {
                const {
                    x,
                    y
                } = getCursorPosition(event);
                const endVertex = checkClickedVertex(x, y);

                // Mencegah menghubungkan indeks yang lebih tinggi ke indeks yang lebih rendah
                if (endVertex !== null && edgeStart !== endVertex && endVertex > edgeStart) {
                    showInputDialog3('Masukkan nilai edge:',edgeStart,endVertex);
                    
                }
                edgeStart = null;
            }
        });


        function changeVertexCount() {
            const count = parseInt(document.getElementById('vertexCount').value);
            document.getElementById('endVertex').value = count - 1;

            if (!isNaN(count) && count >= 2) {
                vertices = [];
                for (let i = 0; i < count; i++) {
                    const {
                        x,
                        y
                    } = getRandomPosition();
                    const vertexEdges = getRandomEdges(count, i); // Mendapatkan edges secara acak
                    vertices.push({
                        x,
                        y,
                        edges: vertexEdges.edges,
                        edgeValues: vertexEdges.edgeValues
                    });
                }
                draw();
            } else {
                showModal('Masukkan angka minimal 2 untuk jumlah vertex.');
            }
        }

        function checkClickedEdge(cursorX, cursorY) {
            for (let i = 0; i < vertices.length; i++) {
                for (let j = 0; j < vertices[i].edges.length; j++) {
                    const startX = vertices[i].x;
                    const startY = vertices[i].y;
                    const endVertex = vertices[vertices[i].edges[j]];
                    const endX = endVertex.x;
                    const endY = endVertex.y;

                    // Calculate distance from point to line (edge)
                    const distance = Math.abs((endY - startY) * cursorX - (endX - startX) * cursorY + endX * startY - endY *
                            startX) /
                        Math.sqrt((endY - startY) ** 2 + (endX - startX) ** 2);

                    // If the distance is within a threshold (e.g., 5 pixels), consider it a click on the edge
                    if (distance <= 5) {
                        return {
                            from: i,
                            to: j
                        }; // Return the indices of the edge clicked
                    }
                }
            }
            return null;
        }

        function getRandomEdges(vertexCount, currentIndex) {
            const edges = [];
            const edgeValues = [];
            const connected = {}; // Menyimpan vertex yang sudah terhubung

            for (let i = currentIndex + 1; i < vertexCount; i++) {
                edges.push(i);
                edgeValues.push(Math.floor(Math.random() * 10) + 1); // Nilai edge acak dari 1 hingga 10
                connected[i] = true;
                connected[currentIndex] = true; // Tandai kedua vertex terhubung
            }
            return {
                edges,
                edgeValues
            };
        }



        function setMode(selectedMode) {
            mode = selectedMode;
            edgeStart = null;
        }

        function getNextLabel(index) {
            return index.toString();
        }

        function drawNextVertexLabel(index) {
            const label = getNextLabel(index);
            return label;
        }

        function removeVertex() {
            if (vertices.length === 0) {
                showModal('Tidak ada vertex yang bisa dihapus.');
                return;
            }

            vertices.pop();
            for (let i = 0; i < vertices.length; i++) {
                for (let j = vertices[i].edges.length - 1; j >= 0; j--) {
                    if (vertices[i].edges[j] >= vertices.length) {
                        vertices[i].edges.splice(j, 1);
                        vertices[i].edgeValues.splice(j, 1);
                    }
                }
            }
            draw();
        }


        function runDijkstra() {
            const INF = Number.MAX_SAFE_INTEGER;
            const distance = [];
            const visited = [];
            const parent = [];

            const ver_edge = getDataFromCanvas();
            const nodes = ver_edge.nodes;
            const edges = ver_edge.edges;

            if (nodes.length === 0 || edges.length === 0) {
                showModal('Tidak ada vertex atau edge yang tersedia. Silakan tambahkan vertex dan edge terlebih dahulu.');
                return;
            }

            for (let i = 0; i < nodes.length; i++) {
                distance[i] = INF;
                visited[i] = false;
                parent[i] = -1;
            }



            const startNode = parseInt(document.getElementById('startVertex').value);
            const endNode = parseInt(document.getElementById('endVertex').value);

            if (endNode > nodes.length-1 || startNode < 0) {
                showModal('Vertex Awal tidak boleh kurang dari 0 atau Vertex Akhir tidak boleh lebih dari jumlah Vertex.');
                return;
            }

            distance[startNode] = 0;

            for (let count = 0; count < nodes.length - 1; count++) {
                let u = -1;
                for (let i = 0; i < nodes.length; i++) {
                    if (!visited[i] && (u === -1 || distance[i] < distance[u])) {
                        u = i;
                    }
                }
        
                visited[u] = true;
        
                for (let v = 0; v < nodes.length; v++) {
                    if (!visited[v] && edges.some(edge => edge.source === u && edge.target === v)) {
                        const edgeIndex = edges.findIndex(edge => edge.source === u && edge.target === v);
                        const weight = edges[edgeIndex].weight;
                        if (distance[u] !== INF && distance[u] + weight < distance[v]) {
                            distance[v] = distance[u] + weight;
                            parent[v] = u;
                        }
                    }
                }

            }

            // Menyorot jalur terpendek pada tampilan graf
            draw();
            let path = [];
            for (let j = endNode; j !== -1; j = parent[j]) {
                path.push(j);
            }
            path.reverse();

            // Highlight the shortest path by changing the color of the lines on that path
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 3;
            for (let k = 0; k < path.length - 1; k++) {
                const node1 = path[k];
                const node2 = path[k + 1];
                const edge = edges.find(e =>
                    (e.source === node1 && e.target === node2) || (e.source === node2 && e.target === node1)
                );
                const weight = edge ? edge.weight : ''; // Get weight from edge object
                ctx.beginPath();
                ctx.moveTo(nodes[node1].x, nodes[node1].y);
                ctx.lineTo(nodes[node2].x, nodes[node2].y);
                ctx.stroke();
                ctx.font = '14px Arial';
                ctx.fillStyle = 'black';
                ctx.fillText(weight, (nodes[node1].x + nodes[node2].x) / 2, (nodes[node1].y + nodes[node2].y) / 2);
            }



        }

        function getDataFromCanvas() {
            const nodes = [];
            const edges = [];

            // Mengambil data posisi vertex dari vertices
            for (let i = 0; i < vertices.length; i++) {
                const node = {
                    id: i,
                    x: vertices[i].x,
                    y: vertices[i].y,
                    edges: []
                };
                nodes.push(node);

                // Mengambil data hubungan antar vertex dan bobot edge-nya dari edges
                for (let j = 0; j < vertices[i].edges.length; j++) {
                    const edge = {
                        source: i, // nodeIndex1
                        target: vertices[i].edges[j], // nodeIndex2
                        weight: vertices[i].edgeValues[j] // weight
                    };
                    node.edges.push(edge);
                    edges.push(edge);
                }
            }

            // Output hasil ekstraksi data dari canvas
            console.log("Nodes:");
            console.log(nodes);
            console.log("Edges:");
            console.log(edges);

            const startNode = parseInt(document.getElementById('startVertex').value);
            const endNode = parseInt(document.getElementById('endVertex').value);

            pywebview.api.sendEdgeValue({
                nodes,
                edges, start:startNode, end: endNode
            });
            // Jika Anda ingin mengembalikan data untuk digunakan di tempat lain, dapat menggunakan return
            return {
                nodes,
                edges
            };
        }

        // Panggil fungsi getDataFromCanvas untuk mendapatkan data dari canvas

        draw();
    </script>
</body>

</html>

    """
    api = Api()

    # Membuat jendela webview dan memuat file HTML
    webview.create_window('Dijkstra', html=html_content,width=800, height=650, js_api=api)
    webview.start(debug=True)

class Api:
    def sendEdgeValue(self,data):
        if(len(data['nodes']) != 0):
            graph: Graph = Graph()

            for node in data['nodes']:
                # print("Node ID:", node['id'])
                # print("X-coordinate:", node['x'])
                # print("Y-coordinate:", node['y'])
                # print("Edges:", node['edges'])
                # print("-----------------")
                graph.add_vertex(str(node['id']))


            for edge in data['edges']:
                graph.add_edge(str(edge['source']), str(edge['target']), edge['weight'])

            try:
                graph.dijkstra(str(data['start']))
                panjang_edge_tercepat = graph.hitung_panjang_edge_tercepat(str(data['start']), str(data['end']));

                pathnya = graph.return_path(str(data['end']))

                hasil = "Jalur tercepat dari {} ke {} adalah [{}] dengan jarak {}".format(
                    str(data['start']),
                    str(data['end']),
                    pathnya,
                    str(panjang_edge_tercepat)
                    );
                
                webview.create_window('Hasil Dijkstra', html=f'''
                <p>{hasil}</p>
                ''', width=400, height=100)
            except:
                print('Terjadi Kesalahan')

    def sendErrorWarning(self,data):
        webview.create_window('Warning!', html=f'''
            <p>{data}</p>
            ''', width=400, height=100)

    def sendAbout(self):
        webview.create_window('Tentang Kami', html=
        '''                      
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }

        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
        }
        </style>
        <div style="text-align: center;">
        <p><b>Dijkstra Visualization:</b></p>
        <table>
            <thead>
                <tr>
                    <th>Nama</th>
                    <th>NRP</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Aditya Nanda Utama</td>
                    <td>6026231036</td>
                </tr>
                <tr>
                    <td>Airlangga Bayu Satriawan</td>
                    <td>6026231006</td>
                </tr>
                <tr>
                    <td>Alvin Tarisa Akbar</td>
                    <td>6026231009</td>
                </tr>
            </tbody>
        </table>
        <p>Infrastruktur Teknologi Informasi <br><br> <b>Institut Teknologi Sepuluh Nopember</b></p>
      </div>
      '''
      , width=400, height=300)

if __name__ == '__main__':
    main()


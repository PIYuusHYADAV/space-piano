const express = require("express");
const app = express();
const path = require("path");
const port = 8080;
const multer = require("multer");
const fs = require("fs");
const { exec } = require("child_process");

const uploadDir = path.join(__dirname, "videofiles");
if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueName = Date.now() + path.extname(file.originalname);
    cb(null, uniqueName);
  },
});

const upload = multer({ storage: storage });
app.use("/videofiles", express.static(path.join(__dirname, "videofiles")));

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static("public"));
app.use(express.static(path.join(__dirname, "public")));

app.listen(port, () => {
  console.log("I am Listening on port", port);
});

app.get("/", (req, res) => {
  res.render("first.ejs");
});

app.post("/getdata", upload.single("image"), (req, res) => {
  if (!req.file) {
    return res.status(400).send("No file uploaded.");
  }

  const imagePath = path.join(__dirname, "videofiles", req.file.filename);
  console.log(`Image uploaded to: ${imagePath}`);

  exec(`python3 process_image.py ${imagePath}`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return res.status(500).send("Error processing image.");
    }

    if (stderr) {
      console.error(`Python script stderr: ${stderr}`);
      return res.status(500).send("Error processing image.");
    }

    console.log(`Python script output: ${stdout}`);
    res.render("display", { imagePath });
  });
});

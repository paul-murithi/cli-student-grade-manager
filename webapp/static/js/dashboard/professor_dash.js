let studentId = undefined;
let courseId = undefined;
let studentName = undefined;
let courseName = undefined;

const gradeButtons = document.querySelectorAll(".grade-btn").forEach((btn) =>
  btn.addEventListener("click", (e) => {
    openActionMenu(e);
  })
);

const modal = document.getElementById("modal");

const closeModalBtn = document
  .getElementById("close-modal")
  .addEventListener("click", () => modal.close());

function openActionMenu(e) {
  studentId = e.target.dataset.studentId;
  courseId = e.target.dataset.courseId;
  studentName = e.target.dataset.studentName;
  courseName = e.target.dataset.courseName;

  modalTitle = document.getElementById(
    "modal-title"
  ).textContent = `Add grades for student: ${studentName}`;
  courseTitle = document.getElementById("course").value = courseName;

  studentIdInput = document.getElementById("student-id").value = studentId;
  courseIdInput = document.getElementById("course-id").value = courseId;

  modal.showModal();
}

function validateScore(score) {
  return score > 1 && score <= 100;
}
function addGrade(e) {}

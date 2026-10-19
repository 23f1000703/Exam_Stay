<template>
  <div class="home">

    <section class="hero">
      <div class="hero-content">
        <p class="tagline">STAY SMART. EXAM READY.</p>

        <h1>
          Find a comfortable stay
          <span>near your exam centre.</span>
        </h1>

        <p class="hero-text">
          ExamStay helps students find verified and affordable
          short-term accommodation near exam centres, interviews,
          and other important events.
        </p>

        <div class="hero-buttons">
          <RouterLink to="/register" class="primary-button">
            Get Started
          </RouterLink>

          <a href="#about" class="secondary-button">
            Learn More
          </a>
        </div>
      </div>
    </section>

    <section id="about" class="about">
      <div class="about-content">

        <p class="section-label">ABOUT EXAMSTAY</p>

        <h2>
          Your stay should be the
          <span>least of your worries.</span>
        </h2>

        <p>
          ExamStay is designed for students who travel to another city
          for exams, interviews, entrance tests, and internships.
        </p>

        <p>
          Finding a safe and affordable place for just a few days can be
          difficult. ExamStay connects students with verified
          accommodations so they can focus on what actually matters.
        </p>

        <div class="features">

          <div class="feature">
            <h3>Verified Stays</h3>
            <p>
              Find accommodations that have gone through our
              verification process.
            </p>
          </div>

          <div class="feature">
            <h3>Student Focused</h3>
            <p>
              Designed specifically for students travelling for
              exams and other important events.
            </p>
          </div>

          <div class="feature">
            <h3>Short-Term</h3>
            <p>
              Book a place for the exact duration you need without
              committing to a long-term stay.
            </p>
          </div>

        </div>

      </div>
    </section>

    <section class="how-it-works">

      <p class="section-label">HOW IT WORKS</p>

      <h2>Find your stay in three steps</h2>

      <div class="steps">

        <div class="step">
          <div class="number">01</div>
          <h3>Search</h3>
          <p>
            Enter your exam city, centre and travel dates.
          </p>
        </div>

        <div class="step">
          <div class="number">02</div>
          <h3>Choose</h3>
          <p>
            Compare verified accommodations based on your needs.
          </p>
        </div>

        <div class="step">
          <div class="number">03</div>
          <h3>Book</h3>
          <p>
            Book your stay and focus on your exam preparation.
          </p>
        </div>

      </div>

    </section>

  </div>
</template>

<style scoped>
.home {
  background: #ffffff;
}

.hero {
  min-height: 650px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 30px;
  background: #f7f7f5;
}

.hero-content {
  max-width: 900px;
  text-align: center;
}

.tagline,
.section-label {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #666;
  margin-bottom: 20px;
}

.hero h1 {
  font-size: 58px;
  line-height: 1.1;
  margin-bottom: 25px;
  color: #171717;
}

.hero h1 span,
.about h2 span {
  display: block;
}

.hero-text {
  max-width: 680px;
  margin: 0 auto;
  font-size: 18px;
  line-height: 1.7;
  color: #666;
}

.hero-buttons {
  margin-top: 35px;
  display: flex;
  justify-content: center;
  gap: 15px;
}

.primary-button,
.secondary-button {
  padding: 13px 28px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
}

.primary-button {
  background: #171717;
  color: white;
}

.secondary-button {
  background: white;
  color: #171717;
  border: 1px solid #ccc;
}

.about {
  padding: 100px 30px;
}

.about-content {
  max-width: 1000px;
  margin: auto;
}

.about h2 {
  font-size: 42px;
  line-height: 1.2;
  margin-bottom: 30px;
}

.about-content > p:not(.section-label) {
  max-width: 800px;
  font-size: 17px;
  line-height: 1.8;
  color: #666;
}

.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 25px;
  margin-top: 55px;
}

.feature {
  padding: 30px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
}

.feature h3 {
  margin-bottom: 12px;
}

.feature p {
  color: #666;
  line-height: 1.6;
}

.how-it-works {
  padding: 100px 30px;
  background: #f7f7f5;
  text-align: center;
}

.how-it-works h2 {
  font-size: 40px;
  margin-bottom: 55px;
}

.steps {
  max-width: 1000px;
  margin: auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.step {
  background: white;
  padding: 35px;
  border-radius: 8px;
}

.number {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 20px;
}

.step h3 {
  margin-bottom: 12px;
}

.step p {
  color: #666;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero h1 {
    font-size: 40px;
  }

  .features,
  .steps {
    grid-template-columns: 1fr;
  }

  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
}
</style>
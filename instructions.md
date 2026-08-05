# Micromanage your agents

> **How you'll submit this lab**
>
> This repo is your lab. Fork it, do the work described below in your fork, then open a pull
> request back into this repository. An AI reviewer will check your PR against `rubric.md` and
> leave feedback directly on the PR. See `README.md` for the full workflow.

**Scenario**  
You're building an evaluation system for a specific domain or use case. Rather than using existing benchmarks, you need to create a custom dataset that reflects your actual requirements. This lab guides you through creating a custom LangSmith dataset from documents of your choice, setting up evaluations, and analyzing results. You'll learn how to use LangSmith for dataset management, experiment tracking, and model comparison.

**Learning Objectives**
- [ ] Choose and prepare documents for dataset creation
- [ ] Create a custom LangSmith dataset from your chosen domain
- [ ] Implement target functions for LLM evaluation
- [ ] Set up and run evaluations using LangSmith
- [ ] Analyze evaluation results and create reports
- [ ] (Optional) Design custom evaluators beyond correctness
- [ ] (Optional) Perform cost and performance optimization analysis

**Estimated Time:** 180-240 minutes (3-4 hours)

**Prerequisites:**
- [ ] Completion of the LangSmith lesson (`02_langsmith.ipynb`)
- [ ] Understanding of LangSmith concepts: tracing, datasets, experiments
- [ ] Familiarity with OpenAI API
- [ ] Basic Python programming experience
- [ ] LangSmith account and API key set up
- [ ] Access to documents or data in your chosen domain

---

## Introduction

This lab takes you through the complete workflow of creating a custom evaluation dataset and running experiments in LangSmith:

1. **Select** a document or domain relevant to your interests or a use case
2. **Create** a custom LangSmith dataset from your chosen materials
3. **Implement** target functions that process inputs and generate outputs
4. **Evaluate** your implementation using built-in and custom evaluators
5. **Analyze** results and create a comprehensive evaluation report

**Why this matters:**
- Real-world evaluations often require custom datasets that match your specific use case
- LangSmith provides a structured way to manage datasets, experiments, and results
- Understanding dataset creation and evaluation workflows is essential for production systems
- Custom evaluators allow you to measure what matters for your specific domain

**Success criteria:**
- [ ] Created a custom LangSmith dataset with at least 10 examples
- [ ] Implemented a working target function with tracing enabled
- [ ] Successfully ran an evaluation using LangSmith
- [ ] Generated an analysis report with key metrics and insights
- [ ] (Optional) Designed and tested a custom evaluator
- [ ] (Optional) Completed cost and performance optimization analysis

---

## Reference Materials

**Documentation:**
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangSmith Python Client](https://python.langchain.com/docs/langsmith/)
- [OpenEvals Documentation](https://github.com/Anthropic-OpenEvals/openevals)
- [OpenAI API Documentation](https://platform.openai.com/docs)

**Lesson Materials:**
- Reference the notebook `02_langsmith.ipynb` for implementation patterns and examples
- The notebook demonstrates: tracing setup, dataset creation, target functions, evaluators, and experiment execution

**Dataset Resources:**
- [Hugging Face Datasets](https://huggingface.co/datasets) - For finding example datasets or inspiration
- Your own documents, text files, or domain-specific materials

---

## Part 1: Setup & Document Selection (30-45 minutes)

### Step 1: Choose Your Domain and Documents (15-20 min)

**Objective:** Select a domain and gather documents that will form the basis of your custom dataset.

**What to do:**

Choose a domain that interests you or relates to a real use case. Consider domains such as:
- **Customer Support:** Support tickets, FAQ responses, email threads
- **Code Review:** Code snippets with review comments, pull request discussions
- **Legal Documents:** Contract summaries, legal Q&A, compliance documents
- **Product Descriptions:** E-commerce listings, product reviews, specifications
- **Educational Content:** Study questions, explanations, course materials
- **Content Creation:** Blog posts, articles, social media content
- **Your Own Domain:** Any text-based domain where you want to evaluate LLM performance

**Requirements for your documents:**
- You need at least 10-15 examples to create a meaningful dataset
- Each example should have a clear input (question, prompt, or task)
- Ideally, examples should have expected outputs or ground truth (answers, summaries, classifications)
- Examples should be diverse enough to test different aspects of your use case
- Documents can be in any format: text files, CSV, JSON, or scraped from websites

**Deliverable:** 
- Document your chosen domain in 2-3 sentences
- List the source(s) of your documents
- Describe what makes a good example in your domain (what are the inputs and expected outputs?)

---

### Step 2: Set Up LangSmith Environment (15-25 min)

**Objective:** Configure your environment for LangSmith tracing and dataset creation.

**What to do:**

1. **Environment Setup:**
   - Ensure you have your LangSmith API key ready
   - Set up environment variables for LangSmith tracing
   - Configure the LangSmith endpoint (EU or US) based on your preference
   - Create a project name for your experiments

2. **Client Initialization:**
   - Initialize the LangSmith Client
   - Set up OpenAI client with LangSmith wrapping for automatic tracing
   - Verify your connection to LangSmith

3. **Project Configuration:**
   - Choose a descriptive project name for your evaluation work
   - Consider using a naming convention that includes your domain or use case

**Implementation Notes:**
- Refer to the notebook `02_langsmith.ipynb` for the exact setup patterns
- The notebook shows how to configure environment variables and initialize clients
- Pay attention to the tracing setup - this will automatically log your experiments

**Deliverable:**
- Working LangSmith client connection
- Environment configured for tracing
- Project name chosen and documented

---

## Part 2: Dataset Creation (60-90 minutes)

### Step 3: Extract and Structure Your Examples (30-45 min)

**Objective:** Transform your documents into a structured format suitable for LangSmith dataset creation.

**What to do:**

1. **Extract Examples:**
   - Process your documents to extract individual examples
   - Each example should represent a single evaluation case
   - Ensure examples are independent and can be evaluated separately

2. **Structure Your Data:**
   - Organize examples with clear input fields (what you'll give to the model)
   - Include output fields if you have ground truth or expected results
   - Add metadata that might be useful for analysis (category, difficulty, source, etc.)

3. **Data Quality Checks:**
   - Verify you have at least 10 examples (aim for 15-20 for better evaluation)
   - Check that inputs are clear and well-formed
   - Ensure outputs (if available) are appropriate for your domain
   - Remove any examples that are unclear or incomplete

**Data Structure Considerations:**
- Inputs: What information will you provide to the model? (e.g., question, context, prompt)
- Outputs: What should the model produce? (e.g., answer, summary, classification)
- Metadata: What additional information might be useful? (e.g., category, difficulty, source document)

**Implementation Notes:**
- You may need to write scripts to parse your documents and extract examples
- Consider using Python's file handling, CSV parsing, or JSON processing
- The notebook shows how to structure data for LangSmith dataset creation

**Deliverable:**
- List or data structure containing 10-20 examples
- Each example should have inputs and (if available) expected outputs
- Document your data structure and what each field represents

---

### Step 4: Create LangSmith Dataset (30-45 min)

**Objective:** Upload your examples to LangSmith as a reusable dataset.

**What to do:**

1. **Dataset Creation:**
   - Create a new dataset in LangSmith with a descriptive name
   - Add a clear description explaining what the dataset contains
   - Choose a name that reflects your domain and use case

2. **Upload Examples:**
   - Convert your structured examples into LangSmith's format
   - Upload inputs and outputs (if available) for each example
   - Verify that all examples were successfully uploaded

3. **Dataset Verification:**
   - Check your dataset in the LangSmith UI
   - Verify that examples are correctly formatted
   - Ensure inputs and outputs are properly associated

**Dataset Naming:**
- Use descriptive names that indicate the domain and purpose
- Consider including version information if you plan to iterate
- Make names unique to avoid conflicts with existing datasets

**Implementation Notes:**
- The notebook demonstrates how to check for existing datasets before creating new ones
- Follow the pattern shown for creating datasets and adding examples
- Pay attention to the structure of inputs and outputs in the notebook examples

**Deliverable:**
- A LangSmith dataset containing your examples
- Dataset name and description documented
- Verification that examples are correctly uploaded (screenshot or confirmation)

---

## Part 3: Evaluation Setup (45-60 minutes)

### Step 5: Implement Target Function (30-40 min)

**Objective:** Create a target function that processes dataset inputs and generates outputs using an LLM.

**What to do:**

1. **Design Your Target Function:**
   - Define what your function should do: take inputs from your dataset and produce outputs
   - Consider what system prompt or instructions are appropriate for your domain
   - Decide on model parameters (model choice, temperature, max tokens, etc.)

2. **Implement the Function:**
   - Create a function that accepts inputs in the format of your dataset
   - Use the wrapped OpenAI client to make API calls
   - Process and return outputs in a consistent format
   - Add the `@traceable` decorator to enable automatic tracing

3. **Function Requirements:**
   - Function should accept a dictionary with your input fields
   - Function should return a dictionary with output fields
   - Function should handle errors gracefully
   - Function should be deterministic or have controlled randomness

**Function Design Considerations:**
- System prompts: What instructions will help the model perform well on your task?
- Model selection: Which model is appropriate for your use case and budget?
- Output format: How should the model structure its response?
- Error handling: What should happen if the API call fails?

**Implementation Notes:**
- The notebook shows examples of target functions with different models
- Pay attention to how inputs are extracted and outputs are structured
- Use tracing decorators to automatically log your function calls

**Deliverable:**
- Working target function that processes your dataset inputs
- Function documented with its purpose and parameters
- Test the function on 2-3 examples to verify it works correctly

---

### Step 6: Set Up Evaluators (15-20 min)

**Objective:** Configure evaluators that will score your target function's outputs.

**What to do:**

1. **Choose Evaluation Approach:**
   - Determine what aspects of outputs you want to evaluate
   - For most cases, start with correctness (does the output match expected results?)
   - Consider what other dimensions matter for your domain

2. **Configure Built-in Evaluators:**
   - Set up a correctness evaluator using LLM-as-judge
   - Configure the evaluator with appropriate prompts and models
   - Ensure the evaluator can compare outputs to reference outputs from your dataset

3. **Evaluator Requirements:**
   - Evaluator should accept inputs, outputs, and reference outputs
   - Evaluator should return structured feedback (scores, reasoning, etc.)
   - Evaluator should be appropriate for your domain and task type

**Evaluation Considerations:**
- What does "correct" mean in your domain?
- Are there multiple valid outputs, or is there one correct answer?
- What criteria beyond correctness might matter? (tone, completeness, format, etc.)

**Implementation Notes:**
- The notebook demonstrates how to create LLM-as-judge evaluators
- Follow the pattern for evaluator functions that accept inputs, outputs, and references
- Consider using openevals for pre-built evaluator prompts

**Deliverable:**
- Configured evaluator function ready to use
- Documentation of what the evaluator measures
- Understanding of how the evaluator will score your outputs

---

## Part 4: Run Evaluation (30-45 minutes)

### Step 7: Execute Evaluation Experiment (20-30 min)

**Objective:** Run your evaluation using LangSmith's experiment framework.

**What to do:**

1. **Configure Experiment:**
   - Set up the evaluation with your target function and dataset
   - Specify which evaluators to use
   - Choose an experiment prefix that identifies this run
   - Set concurrency limits appropriate for your API rate limits

2. **Run the Evaluation:**
   - Execute the evaluation and wait for completion
   - Monitor progress and check for any errors
   - Verify that all examples in your dataset were processed

3. **Collect Results:**
   - Retrieve evaluation results from LangSmith
   - Extract scores, feedback, and metadata for each example
   - Organize results for analysis

**Experiment Configuration:**
- Experiment prefix: Use a name that identifies this specific run (e.g., model name, date, configuration)
- Concurrency: Balance speed with API rate limits (start with 2-3 concurrent requests)
- Error handling: Ensure your evaluation can handle occasional API failures

**Implementation Notes:**
- The notebook shows how to use `client.evaluate()` to run experiments
- Follow the pattern for passing target functions, datasets, and evaluators
- Results will be automatically traced and stored in LangSmith

**Deliverable:**
- Completed evaluation run in LangSmith
- Results collected and accessible
- Experiment visible in LangSmith UI with all traces

---

### Step 8: Review Results in LangSmith UI (10-15 min)

**Objective:** Explore your evaluation results using LangSmith's interface.

**What to do:**

1. **Navigate to Your Project:**
   - Open your LangSmith project in the web interface
   - Locate your experiment run
   - Review the experiment summary and metrics

2. **Examine Individual Examples:**
   - Click through individual examples to see inputs, outputs, and scores
   - Review evaluator feedback and reasoning
   - Identify patterns in successful and failed cases

3. **Analyze Performance:**
   - Look at aggregate metrics (average scores, pass rates, etc.)
   - Identify which examples performed well or poorly
   - Note any systematic issues or patterns

**What to Look For:**
- Overall performance metrics
- Distribution of scores across examples
- Examples with particularly high or low scores
- Common failure modes or error patterns
- Correlation between input characteristics and performance

**Deliverable:**
- Screenshots or notes from LangSmith UI review
- Initial observations about performance
- List of interesting examples to investigate further

---

## Part 5: Analysis & Reporting (45-60 minutes)

### Step 9: Analyze Results (25-35 min)

**Objective:** Perform detailed analysis of your evaluation results.

**What to do:**

1. **Calculate Aggregate Metrics:**
   - Compute mean, median, and distribution of scores
   - Calculate pass/fail rates if applicable
   - Identify best and worst performing examples

2. **Categorical Analysis:**
   - If you have metadata (categories, difficulty levels, etc.), analyze performance by category
   - Identify which types of examples are easier or harder
   - Look for patterns related to input characteristics

3. **Error Analysis:**
   - Review examples with low scores
   - Identify common failure modes
   - Categorize types of errors (hallucination, incomplete answers, wrong format, etc.)

4. **Performance Insights:**
   - Summarize key findings about model performance
   - Identify strengths and weaknesses
   - Note any surprising results or patterns

**Analysis Framework:**
- Quantitative metrics: scores, distributions, rates
- Qualitative insights: error patterns, success factors
- Comparative analysis: performance across different example types
- Actionable findings: what does this tell you about the model and dataset?

**Implementation Notes:**
- You may want to export results to pandas or another analysis tool
- The notebook shows how to extract scores and create summary statistics
- Consider creating visualizations if helpful

**Deliverable:**
- Analysis of evaluation results with key metrics
- Identification of patterns and insights
- Documentation of findings

---

### Step 10: Create Evaluation Report (20-25 min)

**Objective:** Capture your evaluation process and findings in a **single short paragraph** (plus optional compact bullets/tables), not a long formal report.

**What to do:**

1. **Report Structure:**
   - **Executive Summary:** Brief overview of what you evaluated and key findings
   - **Methodology:** Description of your dataset, target function, and evaluators
   - **Results:** Presentation of metrics, scores, and performance data
   - **Analysis:** Discussion of patterns, insights, and findings
   - **Limitations:** Acknowledgment of constraints, caveats, and scope
   - **Recommendations:** Suggestions for improvements or next steps

2. **Include Key Information:**
   - Dataset description: domain, size, characteristics
   - Model and configuration used
   - Evaluation approach and criteria
   - Key metrics and scores
   - Notable findings and patterns
   - Examples of good and poor performance

3. **Professional Presentation:**
   - Use clear, concise language
   - Include relevant metrics and statistics
   - Provide examples to illustrate points
   - Acknowledge limitations appropriately

**Report guidelines:**
- Write **one short paragraph** (plus bullets/tables if helpful) that covers what you evaluated, main metrics, biggest failure pattern, limitations, and one recommendation. Put charts, tables, and LangSmith screenshots in your folder—**do not** submit a separate long essay.

**Deliverable:**
- `evaluation_summary.md` (or PDF) with the paragraph above and optional compact bullet metrics

---

## Optional Part 1: Custom Evaluator Design (60-90 minutes)

### Step 11: Design Custom Evaluator (30-45 min)

**Objective:** Create a custom evaluator that measures aspects beyond correctness.

**What to do:**

1. **Identify Evaluation Dimensions:**
   - Determine what else matters for your domain beyond correctness
   - Examples: tone, completeness, safety, format compliance, domain-specific quality
   - Choose one dimension to focus on for this exercise

2. **Design Evaluator Prompt:**
   - Create a prompt that instructs an LLM judge to evaluate your chosen dimension
   - Include clear criteria for what makes a good or bad output
   - Specify the output format (scores, reasoning, structured feedback)

3. **Implement Custom Evaluator:**
   - Build a function that uses your custom prompt
   - Follow the evaluator function signature (inputs, outputs, reference_outputs)
   - Test your evaluator on a few examples to verify it works

**Custom Evaluator Considerations:**
- What specific aspect are you measuring?
- How will you define good vs. bad performance?
- What scale or format will you use for scores?
- How will you handle edge cases or ambiguous situations?

**Implementation Notes:**
- The notebook shows how to create LLM-as-judge evaluators
- You can use openevals prompts as inspiration or create your own
- Consider using structured output formats for consistent scoring

**Deliverable:**
- Custom evaluator function implemented and tested
- Documentation of what the evaluator measures and how
- Example evaluations on 2-3 test cases

---

### Step 12: Run Evaluation with Custom Evaluator (20-30 min)

**Objective:** Execute an evaluation using your custom evaluator and compare results.

**What to do:**

1. **Run Evaluation:**
   - Execute an evaluation using both your custom evaluator and correctness evaluator
   - Collect results from both evaluators
   - Compare scores across different evaluation dimensions

2. **Analyze Differences:**
   - Identify examples where correctness and custom evaluator scores differ
   - Understand what your custom evaluator is capturing
   - Determine if the custom evaluator provides additional insights

3. **Compare Results:**
   - Create a comparison of scores from different evaluators
   - Identify correlations or discrepancies
   - Document what the custom evaluator reveals about your outputs

**Deliverable:**
- Evaluation results using custom evaluator
- Comparison analysis between evaluators
- Insights about what the custom evaluator reveals

---

### Step 13: Document Custom Evaluator (10-15 min)

**Objective:** Document your custom evaluator design and findings.

**What to do:**

1. **Documentation:**
   - Describe what your custom evaluator measures
   - Explain the evaluation criteria and prompt design
   - Document the scoring approach and format

2. **Results Summary:**
   - Summarize findings from the custom evaluator
   - Compare with correctness scores
   - Explain what additional insights the custom evaluator provides

**Deliverable:**
- Documentation of custom evaluator design
- Summary of evaluation results and insights
- Reflection on the value of custom evaluation dimensions

---

## Optional Part 2: Cost & Performance Optimization (60-90 minutes)

### Step 14: Run A/B Comparison (30-45 min)

**Objective:** Compare different models or configurations to understand cost-performance trade-offs.

**What to do:**

1. **Select Models to Compare:**
   - Choose 2-3 different models to test (e.g., gpt-4o-mini, gpt-4o, different temperatures)
   - Consider models with different cost and capability profiles
   - Ensure comparisons are fair (same dataset, same evaluators)

2. **Run Comparative Evaluations:**
   - Execute evaluations for each model/configuration
   - Use consistent experiment prefixes to identify each run
   - Collect results for all configurations

3. **Extract Performance Metrics:**
   - Calculate performance scores for each model
   - Track cost information if available (token usage, API costs)
   - Measure latency or response times if relevant

**Comparison Considerations:**
- What models or configurations make sense to compare?
- How will you ensure fair comparison?
- What metrics matter most: accuracy, cost, speed, or a combination?

**Implementation Notes:**
- The notebook demonstrates how to create multiple target functions for different models
- Follow the pattern for running multiple experiments with different configurations
- Use consistent evaluators across all comparisons

**Deliverable:**
- Evaluation results for 2-3 different models/configurations
- Performance metrics for each configuration
- Cost information if available

---

### Step 15: Analyze Cost-Performance Trade-offs (20-30 min)

**Objective:** Analyze the relationship between cost and performance to make optimization recommendations.

**What to do:**

1. **Calculate Metrics:**
   - Compute performance scores for each configuration
   - Estimate or calculate costs (token usage, API pricing)
   - Calculate cost per example or cost per correct answer if applicable

2. **Create Comparison Analysis:**
   - Compare performance across configurations
   - Compare costs across configurations
   - Identify the cost-performance frontier (best performance per dollar)

3. **Identify Optimization Opportunities:**
   - Determine if cheaper models provide acceptable performance
   - Identify if more expensive models justify their cost
   - Find the optimal balance for your use case

**Analysis Framework:**
- Performance vs. Cost: Which configurations offer the best value?
- Performance vs. Speed: Are there latency trade-offs to consider?
- Use case requirements: What level of performance is actually needed?
- Budget constraints: What's the maximum acceptable cost?

**Deliverable:**
- Cost-performance analysis with comparisons
- Identification of optimal configurations
- Recommendations based on different scenarios (budget vs. performance priorities)

---

### Step 16: Create Optimization Report (10-15 min)

**Objective:** Document your cost-performance analysis and recommendations.

**What to do:**

1. **Report Structure:**
   - Summary of models/configurations tested
   - Performance comparison (scores, metrics)
   - Cost comparison (token usage, estimated costs)
   - Cost-performance analysis
   - Recommendations for different scenarios

2. **Include Recommendations:**
   - Best option for maximum performance
   - Best option for cost efficiency
   - Best balanced option
   - Considerations for different use case requirements

**Deliverable:**
- **One short paragraph** in **`optimization_summary.md`** at the repository root naming your best cost/performance trade-off and when you would pick each configuration—use tables or LangSmith exports for numbers, not a long report.

---

## Deliverables

### Submission hygiene

- **Filenames:** Use clear, descriptive names (avoid vague names such as `lab.ipynb`, `final_v2.py`, or `untitled.md`).
- **Scope:** Your **GitHub** repository must contain **only materials for this lab**—no unrelated projects, dumps, or personal files.
- **README:** Include a `README.md` with how to run your work (when applicable) and a clear map of each file/folder. Put the **evaluation** and **optimization** narrative paragraphs in **`evaluation_summary.md`** and **`optimization_summary.md`** at the repository root (Markdown)—**not** in `README.md`.

**GitHub only:** Submit the URL to a **GitHub repository** that contains everything for this lab (Markdown, code, exports, images, decks). Do **not** submit a standalone Google Doc, Notion page, or cloud-only link as your primary deliverable—put sources or exports (for example `.md`, `.pdf`, `.pptx`, screenshots) **in the repository**.

Submit the following items:

1. **Dataset Documentation**
   - Description of your chosen domain and documents
   - Dataset name and description from LangSmith
   - Documentation of your data structure and examples

2. **Implementation Code**
   - Python code for dataset creation
   - Target function implementation
   - Evaluator setup code
   - Evaluation execution code
   - All code should be well-commented and organized

3. **Evaluation Results**
   - LangSmith experiment link or screenshot
   - Results data (scores, metrics, etc.)
   - Analysis of results with key findings

4. **Evaluation summary**
   - **`evaluation_summary.md`** at the repository root: **one short paragraph** plus optional compact bullets/tables covering methodology, results, analysis, and recommendations (see Part 5, Step 10—not a multi-page report)

5. **Optional: Custom Evaluator**
   - Custom evaluator implementation
   - Documentation of evaluator design
   - Results and comparison analysis

6. **Optional: Cost-Performance Analysis**
   - A/B comparison results (data or screenshots)
   - Cost-performance analysis
   - **`optimization_summary.md`** at the repository root with **one short paragraph** of optimization recommendations (see Part 6, Step 16)

**Submission Format:**
- Push a **GitHub** repository (you may name it e.g. `lab_langsmith_<your_name>`)
- Include all deliverables above in the repo
- Add a `README.md` with:
  - Your chosen domain and dataset description
  - Brief overview of your approach
  - How to run your code (if applicable)
  - Links to LangSmith datasets and experiments
  - A **file map**: what each submitted file is for

---

## Success Criteria

Your lab is complete when:
- [ ] You've selected a domain and prepared documents for dataset creation
- [ ] You've created a custom LangSmith dataset with at least 10 examples
- [ ] You've implemented a working target function with tracing enabled
- [ ] You've successfully run an evaluation using LangSmith
- [ ] You've analyzed results and created an evaluation report
- [ ] All deliverables are submitted in the required format
- [ ] (Optional) You've designed and tested a custom evaluator
- [ ] (Optional) You've completed cost and performance optimization analysis

---

## Tips & Troubleshooting

**Common Issues:**

1. **Dataset Creation Problems**
   - Ensure your examples are properly structured with inputs and outputs
   - Check that field names are consistent across examples
   - Verify that you're using the correct format for LangSmith dataset creation
   - Reference the notebook for the exact structure needed

2. **Target Function Errors**
   - Make sure your function accepts inputs in the correct format
   - Verify that you're extracting the right fields from input dictionaries
   - Check that your function returns outputs in the expected format
   - Ensure tracing is properly configured

3. **Evaluation Failures**
   - Verify that your evaluator function signature matches requirements
   - Check that reference outputs are available if your evaluator needs them
   - Ensure your dataset has the required fields for evaluation
   - Check API rate limits if evaluations are failing

4. **Results Analysis Challenges**
   - Export results to a format you can analyze (CSV, JSON, pandas DataFrame)
   - Use the LangSmith UI to explore results interactively
   - Consider creating visualizations for better understanding
   - Look for patterns in both successful and failed examples

**Best Practices:**
- Start with a small dataset (10-15 examples) to test your workflow
- Test your target function on a few examples before running full evaluation
- Use descriptive names for datasets and experiments
- Document your choices and rationale as you go
- Review results in LangSmith UI before doing detailed analysis
- Save your code and results for future reference

**Getting Help:**
- Reference the notebook `02_langsmith.ipynb` for implementation patterns
- Check LangSmith documentation for API details
- Review error messages carefully - they often point to specific issues
- Test components individually before combining them

---

## Extension Activities (Optional)

If you finish early or want to go deeper:

1. **Expand Your Dataset:** Add more examples or diversify your dataset
2. **Multiple Evaluators:** Create and compare multiple custom evaluators
3. **Reproducibility Study:** Run the same evaluation multiple times and analyze variance
4. **Domain-Specific Analysis:** Deep dive into performance on specific categories or example types
5. **Production Considerations:** Think about how you would deploy this evaluation in a production system

---

*Good luck! Remember: the goal is to understand the workflow of creating custom datasets and running evaluations. Focus on learning the process, and don't worry about perfect results.*

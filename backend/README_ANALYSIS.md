# RFP Document Analysis Feature

This document outlines the new RFP document analysis feature that uses OpenAI to automatically analyze uploaded RFP documents and generate project estimations.

## Features

### 1. Document Upload & Parsing
- Support for PDF, DOC, and DOCX files
- Automatic text extraction from documents
- File validation and size limits

### 2. AI-Powered Analysis
- **Summary Generation**: AI provides a concise gist of the RFP
- **Scope Analysis**: Detailed project scope breakdown
- **Requirements Extraction**: Key technical and functional requirements
- **Timeline Estimation**: Project timeline suggestions
- **Technology Stack**: Recommended technologies based on requirements
- **Risk Assessment**: Identified risks and potential challenges

### 3. Task Breakdown & Estimation
- **Hierarchical Task Structure**: Tasks broken down into subtasks
- **Time Estimation**: Hours estimated for each task/subtask
- **Cost Calculation**: Automatic cost calculation based on hourly rates
- **Priority & Complexity**: Each task categorized by priority and complexity
- **Category Classification**: Tasks organized by type (Frontend, Backend, Testing, etc.)

### 4. Interactive UI
- **Analysis Dashboard**: Comprehensive view of analysis results
- **Task Management**: View and organize tasks and subtasks
- **Estimation Summary**: Total hours, costs, and confidence levels
- **Document Management**: Upload, replace, and manage RFP documents

## Setup Instructions

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   Create a `.env` file in the backend directory:
   ```env
   # Database Configuration
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=budget_calculator

   # Security
   SECRET_KEY=your-secret-key-here

   # OpenAI Configuration (REQUIRED)
   OPENAI_API_KEY=your-openai-api-key-here
   OPENAI_MODEL=gpt-4
   OPENAI_MAX_TOKENS=4096
   OPENAI_TEMPERATURE=0.3

   # File Upload
   UPLOAD_DIR=uploads
   MAX_UPLOAD_SIZE=10485760

   # CORS Origins
   BACKEND_CORS_ORIGINS=["http://localhost:3000"]
   ```

3. **Database Migration**
   ```bash
   alembic upgrade head
   ```

4. **Start the Server**
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Environment Configuration**
   Create a `.env` file in the frontend directory:
   ```env
   REACT_APP_API_URL=http://localhost:8000/api/v1
   ```

3. **Start the Development Server**
   ```bash
   npm start
   ```

## OpenAI API Setup

1. **Get API Key**
   - Sign up at [OpenAI Platform](https://platform.openai.com/)
   - Create an API key in your account settings
   - Add billing information (required for API usage)

2. **Model Selection**
   - Default: `gpt-4` (recommended for best results)
   - Alternative: `gpt-3.5-turbo` (faster, lower cost)
   - Update `OPENAI_MODEL` in your `.env` file

3. **Rate Limits**
   - Be aware of OpenAI rate limits
   - Consider implementing retry logic for production
   - Monitor usage in OpenAI dashboard

## Usage

### Analyzing an RFP Document

1. **Upload Document**
   - Navigate to an RFP detail page
   - Click "Upload Document" button
   - Select PDF, DOC, or DOCX file

2. **Run Analysis**
   - Click "Analyze Document" button
   - Set hourly rate for cost calculations
   - Wait for analysis to complete (typically 30-60 seconds)

3. **Review Results**
   - View analysis summary with project scope and requirements
   - Review task breakdown with time and cost estimates
   - Check identified risks and technology recommendations

### Managing Analysis Results

- **View Tasks**: Expand task breakdown section to see detailed estimations
- **Export Data**: Copy analysis results for external use
- **Re-analyze**: Delete and re-run analysis with updated documents
- **Update Estimates**: Manually adjust hourly rates and re-calculate costs

## API Endpoints

### Analysis Endpoints
- `POST /rfps/{rfp_id}/analyze` - Analyze RFP document
- `GET /rfps/{rfp_id}/analysis` - Get analysis results
- `GET /rfps/{rfp_id}/analysis/tasks` - Get task breakdown
- `DELETE /rfps/{rfp_id}/analysis` - Delete analysis
- `GET /rfps/analysis/status/{rfp_id}` - Check analysis status

### Document Endpoints
- `POST /rfps/{rfp_id}/upload` - Upload RFP document

## Database Schema

### New Tables
- `rfp_analyses` - Stores analysis results and metadata
- `analysis_tasks` - Stores task breakdown information
- `analysis_subtasks` - Stores subtask details and estimates

### Relationships
- RFP → RFPAnalysis (1:1)
- RFPAnalysis → AnalysisTask (1:many)
- AnalysisTask → AnalysisSubtask (1:many)

## Cost Considerations

### OpenAI API Costs
- GPT-4: ~$0.03-0.06 per analysis (depending on document size)
- GPT-3.5-turbo: ~$0.01-0.02 per analysis
- Costs scale with document length and complexity

### Optimization Tips
- Use GPT-3.5-turbo for cost-sensitive applications
- Implement caching to avoid re-analyzing unchanged documents
- Set reasonable token limits to control costs
- Monitor usage through OpenAI dashboard

## Troubleshooting

### Common Issues

1. **Analysis Fails**
   - Check OpenAI API key is valid
   - Verify document is properly uploaded
   - Check server logs for specific errors

2. **Poor Analysis Quality**
   - Try GPT-4 instead of GPT-3.5-turbo
   - Ensure document text is clearly readable
   - Check document format is supported

3. **Performance Issues**
   - Large documents may take longer to process
   - Consider breaking very large documents into sections
   - Monitor OpenAI rate limits

### Support
- Check server logs in `backend/logs/`
- Verify database connectivity
- Test OpenAI API key with simple requests
- Review document text extraction quality

## Future Enhancements

- **Custom Prompts**: Allow customization of analysis prompts
- **Multiple Models**: Support for different AI models/providers
- **Batch Processing**: Analyze multiple RFPs simultaneously
- **Template Management**: Save and reuse analysis templates
- **Integration**: Connect with project management tools
- **Reporting**: Generate analysis reports and comparisons 
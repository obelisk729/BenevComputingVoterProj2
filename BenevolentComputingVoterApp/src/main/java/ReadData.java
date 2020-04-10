import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.security.GeneralSecurityException;
import java.util.Collections;
import java.util.List;
import java.util.Arrays;

import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.extensions.java6.auth.oauth2.AuthorizationCodeInstalledApp;
import com.google.api.client.extensions.jetty.auth.oauth2.LocalServerReceiver;
import com.google.api.client.googleapis.auth.oauth2.GoogleAuthorizationCodeFlow;
import com.google.api.client.googleapis.auth.oauth2.GoogleClientSecrets;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.javanet.NetHttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.client.util.store.FileDataStoreFactory;
import com.google.api.services.sheets.v4.Sheets;
import com.google.api.services.sheets.v4.SheetsScopes;
import com.google.api.services.sheets.v4.model.AppendValuesResponse;
import com.google.api.services.sheets.v4.model.UpdateValuesResponse;
import com.google.api.services.sheets.v4.model.ValueRange;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class ReadData 
{
	/* Just to talk obliquely for a second, a lot of the code written here is stuff that I don't necessarily understand
	 * why it works because they've been taken from tutorials on the Internet. Unless commented on, I'd recommend not
	 * changing anything that you don't understand here.
	 * Tutorials used:
	 * https://www.youtube.com/watch?v=8yJrQk9ShPg
	 * https://www.youtube.com/watch?v=zDxTSUWaZs4
	 * https://www.youtube.com/watch?v=tI1qGwhn_bs
	*/
	
	private static Sheets sheetsService;
	private static String APPLICATION_NAME = "Google Sheets Example";
	// Below is a section the URL for the spreadsheet we want, should be between /d/ and /edit#gid=0
	private static String SPREADSHEET_ID = "1V0K2Vw4_Ar1Y3tFataB887wFZApcKeMeXGVHN5ovZYY";
	
	private static Credential authorize() throws IOException, GeneralSecurityException
	{
		InputStream in = ReadData.class.getResourceAsStream("/credentials.json");
		GoogleClientSecrets clientSecrets = GoogleClientSecrets.load(JacksonFactory.getDefaultInstance(), new InputStreamReader(in));
		List<String> scopes = Arrays.asList(SheetsScopes.SPREADSHEETS);
		System.out.println(scopes);
		GoogleAuthorizationCodeFlow flow = new GoogleAuthorizationCodeFlow.Builder(GoogleNetHttpTransport.newTrustedTransport(), JacksonFactory.getDefaultInstance(), clientSecrets, scopes).setDataStoreFactory(new FileDataStoreFactory(new java.io.File("tokens"))).setAccessType("offline").build();
		Credential credential = new AuthorizationCodeInstalledApp(flow, new LocalServerReceiver()).authorize("user");
		return credential;
	}
	
	public static Sheets getSheetsService() throws IOException, GeneralSecurityException
	{
		Credential credential = authorize();
		return new Sheets.Builder(GoogleNetHttpTransport.newTrustedTransport(), JacksonFactory.getDefaultInstance(), credential).setApplicationName(APPLICATION_NAME).build();
		
	}
	
	public static void main(String[] args) throws IOException, GeneralSecurityException
	{
		sheetsService = getSheetsService();
		// The below should be changed later. Limiting the range just because we don't want to deal with possible
		// bugs with empty fields right now. Right now it reads everything from A3 to G8 and prints it.
		String range = "Sheet1!A3:G8";
		ValueRange response = sheetsService.spreadsheets().values().get(SPREADSHEET_ID, range).execute();
		List<List<Object>> values = response.getValues();
		if(values == null || values.isEmpty())
		{
			System.out.println("No data found.");
		}
		else
		{
			for (List row : values)
			{
				System.out.printf("%s", row.get(1));
				System.out.println("");
			}
		}
		
		// Update a specific field to what we want. I've set it to change field G5 to "updated."
		ValueRange body = new ValueRange().setValues(Arrays.asList(Arrays.asList("updated")));
		UpdateValuesResponse result = sheetsService.spreadsheets().values().update(SPREADSHEET_ID, "G5", body).setValueInputOption("RAW").execute();
		System.out.println("");
		System.out.println("");
		
		// Add an entirely new row. Don't think this function will be needed for this program but I added it just in case.
		ValueRange appendBody = new ValueRange().setValues(Arrays.asList(Arrays.asList("10", "2/30/99", "999999999", "9999999999", "2/30/9999", "TEST")));
		AppendValuesResponse appendResult = sheetsService.spreadsheets().values().append(SPREADSHEET_ID, "Sheet1", appendBody).setValueInputOption("USER_ENTERED").setInsertDataOption("INSERT_ROWS").setIncludeValuesInResponse(true).execute();
		System.out.println("");
		System.out.println("");
		
		// This just goes to the voter lookup site and prints out all of the HTML for the page. Still working on
		// how to elegantly implement submitting data. Reading that data should be easy enough now, though.
		final String url = "https://voterlookup.elections.ny.gov/";
		try
		{
			final Document document = Jsoup.connect(url).get();
			System.out.println(document.outerHtml());
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
		}
	}
}

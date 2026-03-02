# client.py
import asyncio
from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult


# ref  https://thenewstack.io/how-to-implement-elicitation-with-model-context-protocol/

# async def send_to_gemini(flight_status_result: str, user_query: str = None):
#     """Send flight status result to Gemini for analysis."""
#     try:
#         gemini_client = genai.Client()

#         # Use the user query if provided, otherwise create a default prompt
#         if user_query:
#             prompt = f"{user_query}\n\nFlight Status Data:\n{flight_status_result}"
#         else:
#             prompt = f"Please analyze this flight status information and provide insights:\n\n{flight_status_result}"

#         response = gemini_client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt
#         )

#         return response.text

#     except Exception as e:
#         return f"Error sending to Gemini: {e}"

async def elicitation_handler(message: str, response_type: type, params, context):
    print(f"Server asks: {message}")

    try:
        type_name = input("Enter schema.org type: ")
        if not type_name.strip():
            print("No flight number provided")
            return ElicitResult(action="decline")
        return response_type(type_name=type_name.strip())

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return ElicitResult(action="cancel")
    except Exception as e:
        print(f"Error handling input: {e}")
        return ElicitResult(action="decline")

async def main():
    client = Client("http://0.0.0.0:8898/sse/", elicitation_handler=elicitation_handler)

    async with client:
        while True:
            print("\nFlight Status Tool with Gemini Analysis")
            print("1. Get flight status")
            # print("2. Get flight status with custom Gemini query")
            print("3. Exit")

            choice = input("\nSelect an option (1-3): ").strip()

            if choice == "1":
                try:
                    # Get flight status from MCP server
                    result = await client.call_tool("get_type_count")
                    print("\nFlight Status Result:")
                    #print(result)
                    flight_status_text = result.content[0].text
                    print(flight_status_text)
                except Exception as e:
                    print(f"Error getting flight status: {e}")

            # elif choice == "2":
            #     try:
            #         # Get custom query from user
            #         user_query = input("\nEnter your question about the flight (e.g., 'Is this flight likely to be delayed?'): ").strip()

            #         # Get flight status from MCP server
            #         result = await client.call_tool("get_flight_status")
            #         print("\nFlight Status Result:")
            #         print(result)

            #         # Send to Gemini with custom query
            #         print("\nSending to Gemini with your question...")
            #         gemini_response = await send_to_gemini(result, user_query)
            #         print("\nGemini Analysis:")
            #         print(gemini_response)

            #     except Exception as e:
            #         print(f"Error getting flight status: {e}")

            elif choice == "3":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    asyncio.run(main())
